from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from app.routes.predict import router as predict_router
from app.routes.plants import router as plants_router
from app.routes.recommend import router as recommend_router

load_dotenv(Path(__file__).resolve().parent.parent.parent / '.env')

app = FastAPI(
    title="AI Smart Gardening API",
    version="1.0.0"
)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    aallow_origins=["*"],
)

app.include_router(predict_router, prefix="/predict", tags=["predict"])
app.include_router(plants_router, prefix="/plants", tags=["plants"])
app.include_router(recommend_router, prefix="/recommend", tags=["recommend"])

@app.get("/")
def root():
    return {"message": "Smart Gardening API running"}
