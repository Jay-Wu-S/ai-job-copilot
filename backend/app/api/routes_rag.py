from fastapi import APIRouter
from app.schemas.rag import RagRequest, RagResponse
from app.services.rag_service import answer_question, get_rag_status

router = APIRouter(tags=["rag"])


@router.post("/rag/ask", response_model=RagResponse)
def ask_rag(payload: RagRequest):
    return answer_question(payload.question)


@router.get("/rag/status")
def rag_status():
    return get_rag_status()