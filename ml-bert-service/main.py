import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from model import BertEmbeddingModel
from ecf_loader import ECFEmbeddingStore
from utils import cosine_similarity_vec
from typing import List, Dict
import numpy as np

from finetune.schema import FineTuneRequest
from finetune.trainer import run_finetuning

app = FastAPI(title="ml-bert-service (BERT + Levels)")

MODEL = BertEmbeddingModel()
ECF_STORE = ECFEmbeddingStore(model=MODEL, ecf_json_path="ecf_data.json", alpha=0.7)

HAS_FINETUNED = MODEL.load_finetuned(path="models/fine_tuned_bert")

class PredictRequest(BaseModel):
    text: str
    top_k: int = 5

@app.get("/health")
def health():
    return {"status": "ok"}

def build_combined_text(job_text: str, mapping: dict) -> str:
    comp_desc = mapping.get("competency_description", "") or ""
    level_desc = mapping.get("level_description", "") or ""

    return (
        f"[JOB PROFILE]\n{job_text}\n\n"
        f"[COMPETENCY]\n{comp_desc}\n\n"
        f"[LEVEL]\n{level_desc}"
    )

@app.post("/predict")
def predict(req: PredictRequest):
    if not req.text or not req.text.strip():
        return {"results": []}

    mappings = ECF_STORE.get_all_mappings()

    if HAS_FINETUNED and MODEL.classifier is not None:
        combined_texts = [build_combined_text(req.text, m) for m in mappings]

        logits = MODEL.predict_with_classifier(combined_texts)  # shape (N, 1) або (N,)
        scores = logits.squeeze(-1) 

        results = []
        for m, score in zip(mappings, scores):
            results.append({
                "competency_id": m["competency_id"],
                "competency_code": m["competency_code"],
                "competency_name": m["competency_name"],
                "competence"
                "level_id": m["level_id"],
                "level": m["level"],
                "level_description": m["level_description"],
                "score": float(score)  
            })

        results.sort(key=lambda x: x["score"], reverse=True)
        return {
            "mode": "finetuned_regression",
            "top_k": req.top_k,
            "results": results[: req.top_k]
        }

    # embed job text
    job_emb = MODEL.embed(req.text)

    scored = []
    for m in ECF_STORE.get_all_mappings():
        combined = m["combined_emb"]
        sim = cosine_similarity_vec(job_emb, combined)
        scored.append({
            "competency_id": m["competency_id"],
            "competency_code": m["competency_code"],
            "competency_name": m["competency_name"],
            "competency_description": m["competency_description"],
            "level_id": m["level_id"],
            "level": m["level"],
            "level_description": m["level_description"],
            "similarity": round(sim, 4)
        })

    # sort and return top_k
    scored.sort(key=lambda x: x["similarity"], reverse=True)
    top = scored[: req.top_k]

    return {"text": req.text, "top_k": req.top_k, "results": top}

@app.post("/finetune/train")
def finetune_model(req: FineTuneRequest):
    result = run_finetuning(req.samples)
    return {
        "message": "Fine-tuning completed",
        "dataset_name": req.dataset_name,
        "result": result
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
