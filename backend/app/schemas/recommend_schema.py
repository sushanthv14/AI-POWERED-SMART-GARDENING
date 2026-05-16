from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date


class RecommendRequest(BaseModel):
    plant_name: str
    is_healthy: bool = True
    disease_name: Optional[str] = None
    confidence: Optional[float] = None
    sunlight_level: str = "medium"
    soil_type: str = "loamy"
    environment: str = "outdoor"
    last_watered: date = Field(default_factory=date.today)


class RecommendResponse(BaseModel):
    plant_name: str
    health_status: str
    health_score: int
    watering_advice: str
    fertilizer_advice: str
    soil_advice: str
    sunlight_advice: str
    care_tips: List[str]
    warnings: List[str]
    next_steps: List[str]
