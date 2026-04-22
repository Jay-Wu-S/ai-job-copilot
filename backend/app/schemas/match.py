from pydantic import BaseModel
from typing import List, Dict

class MatchRequest(BaseModel):
    resume_text: str
    jd_text: str

class ClassifiedResumeSentence(BaseModel):
    text: str
    label: str
    confidence: float

class MatchResponse(BaseModel):
    matched_core_skills: List[str]
    missing_technical_skills: List[str]
    related_background: List[str]
    transferable_matches: List[str]
    transferable_evidence: Dict[str, List[str]]
    learning_suggestions: List[str]
    direct_match_score: float
    transferable_background_score: float
    resume_experience_distribution: Dict[str, int]
    classified_resume_sentences: List[ClassifiedResumeSentence]
    resume_extracted_skills: List[str]
    jd_extracted_skills: List[str]
    hidden_missing_skills: List[str]
    grouped_missing_technical_skills: Dict[str, List[str]]
