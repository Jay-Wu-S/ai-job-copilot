from pydantic import BaseModel
from typing import Dict


class ClassifierRequest(BaseModel):
    text: str


class ClassifierResponse(BaseModel):
    label: str
    confidence: float
    probabilities: Dict[str, float]