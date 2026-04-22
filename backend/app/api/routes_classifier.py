from fastapi import APIRouter
from app.schemas.classifier import ClassifierRequest, ClassifierResponse
from app.services.classifier_service import predict_skill_category

router = APIRouter(tags=["classifier"])


@router.post("/classify-skill", response_model=ClassifierResponse)
def classify_skill(payload: ClassifierRequest):
    return predict_skill_category(payload.text)