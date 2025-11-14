import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from model import BertEmbeddingModel
from ecf_loader import ECFEmbeddingStore
from utils import cosine_similarity_vec
from typing import List, Dict
import numpy as np

app = FastAPI(title="ml-bert-service (BERT + Levels)")

MODEL = BertEmbeddingModel()
ECF_STORE = ECFEmbeddingStore(model=MODEL, ecf_json_path="ecf_data.json", alpha=0.7)

class PredictRequest(BaseModel):
    text: str
    top_k: int = 5

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict")
def predict(req: PredictRequest):
    if not req.text or not req.text.strip():
        return {"results": []}

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
            "level_id": m["level_id"],
            "level": m["level"],
            "level_description": m["level_description"],
            "similarity": round(sim, 4)
        })

    # sort and return top_k
    scored.sort(key=lambda x: x["similarity"], reverse=True)
    top = scored[: req.top_k]

    return {"text": req.text, "top_k": req.top_k, "results": top}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
