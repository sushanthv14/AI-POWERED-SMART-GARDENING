from pydantic import BaseModel

class PredictionResponse(BaseModel):
    plant_name: str
    plant_confidence: float
    disease_name: str
    disease_confidence: float
    is_healthy: bool
    summary: str
    recommended_next_step: str