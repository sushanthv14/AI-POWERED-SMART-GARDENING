from fastapi import APIRouter, HTTPException
from app.schemas.plant_schema import GrowthLogCreate, Plant, PlantCreate
from app.services.plant_service import add_growth_log, create_plant, get_plant, list_plants

router = APIRouter()


@router.get("", response_model=list[Plant])
def get_plants() -> list[Plant]:
    return list_plants()


@router.post("", response_model=Plant)
def create_new_plant(payload: PlantCreate) -> Plant:
    return create_plant(payload)


@router.get("/{plant_id}", response_model=Plant)
def get_one_plant(plant_id: str) -> Plant:
    plant = get_plant(plant_id)
    if not plant:
        raise HTTPException(status_code=404, detail="Plant not found")
    return plant


@router.post("/{plant_id}/growth-log", response_model=Plant)
def create_growth_log(plant_id: str, payload: GrowthLogCreate) -> Plant:
    created_log = add_growth_log(plant_id, payload)
    if not created_log:
        raise HTTPException(status_code=404, detail="Plant not found")
    plant = get_plant(plant_id)
    if plant is None:
        raise HTTPException(status_code=404, detail="Plant not found")
    return plant
