import json
import uuid
from datetime import date
from pathlib import Path
from typing import Dict, List, Optional

from app.schemas.plant_schema import GrowthLog, GrowthLogCreate, Plant, PlantCreate

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / ".." / "data"
MOCK_PLANTS_PATH = DATA_DIR / "mock_plants.json"


def _load_storage() -> Dict[str, List[Dict]]:
    if not MOCK_PLANTS_PATH.exists():
        return {"plants": []}
    with MOCK_PLANTS_PATH.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _save_storage(data: Dict[str, List[Dict]]) -> None:
    with MOCK_PLANTS_PATH.open("w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2, default=str)


def list_plants() -> List[Plant]:
    storage = _load_storage()
    return [Plant(**plant_data) for plant_data in storage.get("plants", [])]


def get_plant(plant_id: str) -> Optional[Plant]:
    storage = _load_storage()
    for plant_data in storage.get("plants", []):
        if plant_data.get("id") == plant_id:
            return Plant(**plant_data)
    return None


def create_plant(payload: PlantCreate) -> Plant:
    storage = _load_storage()
    plant_id = f"plant_{uuid.uuid4().hex[:8]}"
    plant_record = {
        "id": plant_id,
        "nickname": payload.nickname,
        "plant_name": payload.plant_name,
        "disease_status": None,
        "health_score": 100.0,
        "last_watered": date.today().isoformat(),
        "growth_logs": [],
    }
    storage.setdefault("plants", []).append(plant_record)
    _save_storage(storage)
    return Plant(**plant_record)


def add_growth_log(plant_id: str, payload: GrowthLogCreate) -> Optional[GrowthLog]:
    storage = _load_storage()
    for plant_data in storage.get("plants", []):
        if plant_data.get("id") == plant_id:
            log_id = f"log_{uuid.uuid4().hex[:8]}"
            log_entry = {
                "id": log_id,
                "date": payload.date,
                "height_cm": payload.height_cm,
                "leaf_count": payload.leaf_count,
                "notes": payload.notes,
            }
            plant_data.setdefault("growth_logs", []).append(log_entry)
            _save_storage(storage)
            return GrowthLog(**log_entry)
    return None
