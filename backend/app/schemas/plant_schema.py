from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class GrowthLogCreate(BaseModel):
    date: str
    height_cm: float
    leaf_count: int
    notes: Optional[str] = None


class GrowthLog(GrowthLogCreate):
    id: str


class PlantCreate(BaseModel):
    plant_name: str
    nickname: str


class Plant(BaseModel):
    id: str
    plant_name: str
    nickname: str
    disease_status: Optional[str] = None
    health_score: float
    last_watered: str
    growth_logs: List[GrowthLog] = []
