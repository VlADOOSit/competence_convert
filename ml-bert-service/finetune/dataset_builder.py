from typing import List
from .schema import FineTuneSample

def combine_text(sample: FineTuneSample) -> str:
    return (
        f"[JOB PROFILE]\n{sample.profile_text}\n\n"
        f"[COMPETENCY]\n{sample.competency.description}\n\n"
        f"[LEVEL]\n{sample.level.level_description}"
    )

def build_training_pairs(samples: List[FineTuneSample]):
    texts = []
    labels = []

    for s in samples:
        combined = combine_text(s)
        texts.append(combined)
        labels.append(float(s.expert_rating))

    return texts, labels
