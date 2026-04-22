from pydantic import BaseModel
from typing import List


class RagRequest(BaseModel):
    question: str


class RetrievedChunk(BaseModel):
    source: str
    content: str


class RagResponse(BaseModel):
    answer: str
    sources: List[str]
    retrieved_chunks: List[RetrievedChunk]