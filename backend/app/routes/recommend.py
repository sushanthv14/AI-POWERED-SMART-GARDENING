from fastapi import APIRouter
from app.schemas.recommend_schema import RecommendRequest, RecommendResponse
from app.services.recommendation_service import build_recommendation

router = APIRouter()


@router.post("/care", response_model=RecommendResponse)
def care_recommendation(payload: RecommendRequest) -> RecommendResponse:
    return build_recommendation(payload)
