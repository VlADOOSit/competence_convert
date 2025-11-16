from typing import List, Dict
from pydantic import BaseModel

class CompetencyModel(BaseModel):
    competency_id: int
    code: str
    name: str
    description: str

class LevelModel(BaseModel):
    level_id: int
    level_code: str
    level_name: str
    level_description: str

class FineTuneSample(BaseModel):
    profile_text: str
    competency: CompetencyModel
    level: LevelModel
    expert_rating: float

class FineTuneRequest(BaseModel):
    dataset_name: str
    samples: List[FineTuneSample]

