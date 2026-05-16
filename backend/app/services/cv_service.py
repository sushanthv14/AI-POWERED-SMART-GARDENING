import json
import os
import random
import torch
from PIL import Image
from torchvision import models, transforms
import torch.nn as nn
import io
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

class CVService:
    def __init__(
        self,
        model_path="models/plant_disease_model.pt",
        mapping_path="models/class_mapping.json"
    ):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        app_root = BASE_DIR.parent
        repo_root = app_root.parent

        mapping_path = Path(mapping_path)
        if not mapping_path.is_absolute():
            if mapping_path.parts[0] == "backend":
                mapping_path = repo_root / mapping_path
            else:
                mapping_path = app_root / mapping_path

        with open(mapping_path, "r", encoding="utf-8") as f:
            self.class_mapping = json.load(f)

        model_path_value = os.getenv("MODEL_PATH", model_path)
        self.model_path = Path(model_path_value)
        if not self.model_path.is_absolute():
            if self.model_path.parts[0] == "backend":
                self.model_path = repo_root / self.model_path
            else:
                self.model_path = app_root / self.model_path

        self.is_mock = False
        self.model = self._load_model(self.model_path)

        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(
                [0.485, 0.456, 0.406],
                [0.229, 0.224, 0.225]
            )
        ])

    def _load_model(self, model_path: Path):
        model = models.efficientnet_b0(weights=None)
        in_features = model.classifier[1].in_features
        model.classifier[1] = nn.Linear(
            in_features,
            len(self.class_mapping)
        )

        if not model_path.exists():
            self.is_mock = True
            return model

        try:
            state = torch.load(str(model_path), map_location=self.device)
            if isinstance(state, dict):
                model.load_state_dict(state)
            elif isinstance(state, nn.Module):
                model = state
            else:
                self.is_mock = True
        except Exception:
            self.is_mock = True

        model.to(self.device)
        model.eval()

        return model

    def _mock_prediction(self):
        if not self.class_mapping:
            return {
                "plant_name": "Unknown",
                "plant_confidence": 0.0,
                "disease_name": "Unknown",
                "disease_confidence": 0.0,
                "is_healthy": False,
                "summary": "No model available for inference.",
                "recommended_next_step": "Provide a valid model file to enable prediction."
            }

        sample_key = random.choice(list(self.class_mapping.keys()))
        class_info = self.class_mapping[sample_key]
        return {
            "plant_name": class_info.get("plant_name", "Unknown"),
            "plant_confidence": 0.65,
            "disease_name": class_info.get("disease_name", "Unknown"),
            "disease_confidence": 0.65,
            "is_healthy": class_info.get("is_healthy", False),
            "summary": class_info.get("summary", "Mock prediction because no valid model was loaded."),
            "recommended_next_step": class_info.get(
                "recommended_next_step",
                "Provide a valid model file to enable real prediction."
            )
        }

    def predict_from_bytes(self, image_bytes):
        if self.is_mock:
            return self._mock_prediction()

        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

        tensor = self.transform(image).unsqueeze(0).to(self.device)

        with torch.no_grad():
            outputs = self.model(tensor)
            probabilities = torch.nn.functional.softmax(outputs[0], dim=0)
            confidence, idx = torch.max(probabilities, dim=0)

        class_info = self.class_mapping[str(idx.item())]

        return {
            "plant_name": class_info["plant_name"],
            "plant_confidence": round(float(confidence.item()), 2),
            "disease_name": class_info["disease_name"],
            "disease_confidence": round(float(confidence.item()), 2),
            "is_healthy": class_info["is_healthy"],
            "summary": class_info["summary"],
            "recommended_next_step": class_info["recommended_next_step"]
        }