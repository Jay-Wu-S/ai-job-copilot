from fastapi import APIRouter
from app.schemas.match import MatchRequest, MatchResponse
from app.services.match_service import analyze_match

router = APIRouter(tags=["match"])


@router.post("/match", response_model=MatchResponse)
def match_resume_and_jd(payload: MatchRequest):
    return analyze_match(payload.resume_text, payload.jd_text)
