from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.cv_service import CVService
from app.schemas.predict_schema import PredictionResponse

router = APIRouter()

cv_service = CVService()

@router.post("/", response_model=PredictionResponse)
async def predict_disease(file: UploadFile = File(...)):
    try:
        image_bytes = await file.read()
        prediction = cv_service.predict_from_bytes(image_bytes)
        return prediction
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))