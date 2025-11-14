import json
from model import BertEmbeddingModel
from utils import combine_embeddings
import numpy as np
from typing import List, Dict

class ECFEmbeddingStore:
    def __init__(self, ecf_json_path: str = "ecf_data.json", model: BertEmbeddingModel = None, alpha: float = 0.7):
        
        self.path = ecf_json_path
        self.model = model or BertEmbeddingModel()
        self.alpha = alpha
        self.mappings = []  # list of dicts: competency + level + embeddings
        self._load_and_embed()

    def _load_and_embed(self):
        with open(self.path, "r", encoding="utf-8") as f:
            data = json.load(f)

        comp_texts = [comp.get("description", comp.get("name", "")) for comp in data]
        comp_embs = self.model.embed_batch(comp_texts)  # (n_comps, dim)
        comp_id_to_emb = {}
        for comp, emb in zip(data, comp_embs):
            comp_id_to_emb[comp["competency_id"]] = emb

        for comp in data:
            comp_emb = comp_id_to_emb.get(comp["competency_id"])
            for lvl in comp.get("levels", []):
                level_text = lvl.get("description", "")
                
                if not level_text or level_text.strip() == "-":
                    level_emb = comp_emb
                else:
                    level_emb = self.model.embed(level_text)
                combined = combine_embeddings(comp_emb, level_emb, alpha=self.alpha)
                mapping = {
                    "competency_id": comp["competency_id"],
                    "competency_code": comp.get("code"),
                    "competency_name": comp.get("name"),
                    "competency_description": comp.get("description"),
                    "level_id": lvl.get("level_id"),
                    "level": lvl.get("level"),
                    "level_description": level_text,
                    "comp_emb": comp_emb,         # numpy arrays
                    "level_emb": level_emb,
                    "combined_emb": combined
                }
                self.mappings.append(mapping)

    def get_all_mappings(self) -> List[Dict]:
        return self.mappings

    def find_by_competency(self, competency_code: str):
        return [m for m in self.mappings if m["competency_code"] == competency_code]
