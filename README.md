# AI-Powered Smart Gardening & Horticulture Ecosystem

A full-stack plant disease detection and care recommendation platform built with React, FastAPI, and PyTorch. Upload plant leaf images, get disease predictions, and receive tailored horticulture advice.

## Project Overview

- `frontend/` — React app for user interaction, image upload, and result display.
- `backend/` — FastAPI service for image prediction, plant recommendation, and model inference.
- `backend/train_model.py` — training pipeline using EfficientNet and PyTorch.
- `backend/app/models/plant_disease_model.pt` — trained model weights.
- `backend/app/models/class_mapping.json` — generated class mapping for prediction output.

## Features

- Image-based plant disease detection
- Disease-specific plant care and recommendations
- Local environment configuration with `.env`
- Frontend/backend separation for modern deployment workflows

## Installation

1. Clone the repository:

```bash
git clone https://github.com/sushanthv14/AI-POWERED-SMART-GARDENING.git
cd AI-Powered-Smart-Gardening-Horticulture-Ecosystem
```

2. Install frontend dependencies:

```bash
cd frontend
npm install
```

3. Install backend dependencies:

```bash
cd ../backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file in `backend/` with any required settings. Example values should be stored in `.env.example` only.

```env
# backend/.env.example
API_KEY=your_api_key_here
MODEL_URL=https://example.com/path/to/model.pt
```

## Training the Model

Run training from the backend directory after activating the Python virtual environment:

```bash
cd backend
source venv/bin/activate
python backend/train_model.py
```

This script will:

- build the dataset loaders from `backend/datasets/plant_disease_dataset`
- perform head-only training first
- perform full fine-tuning afterward
- save weights to `backend/app/models/plant_disease_model.pt`

## Local Development

### Start the backend

```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Start the frontend

```bash
cd frontend
npm start
```

Then open `http://localhost:3000` to use the application.

## Deployment Notes

### Frontend

- Best hosted on Vercel
- Set the project root to `frontend/`
- Use build command: `npm run build`
- Use output directory: `build/`

### Backend

- Host on Render, Railway, Heroku, or a container service
- Vercel is not ideal for long-running backend inference or large model loads
- Ensure the backend has access to the saved model weights
- Prefer cloud storage for weights if you do not want to commit large binaries to Git

## Model Serving

The backend should load `backend/app/models/plant_disease_model.pt` at startup for inference.

If deploying to production, consider storing weights in cloud storage and downloading them during deployment rather than committing them to Git.

## Notes

- Keep `.env` local and never commit secrets.
- Confirm `.gitignore` contains `backend/venv/`, `.env`, and `*.pt`.
- Use `README.md` as the project entrypoint for contributors and deployers.
