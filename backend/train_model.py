import json
import math
import ssl
from pathlib import Path
from typing import Dict, Tuple

ssl._create_default_https_context = ssl._create_unverified_context

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision import datasets, models, transforms

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "datasets" / "plant_disease_dataset"
MODEL_PATH = BASE_DIR / "app" / "models" / "plant_disease_model.pt"
MAPPING_PATH = BASE_DIR / "app" / "models" / "class_mapping.json"


def parse_class_name(class_name: str) -> Tuple[str, str]:
    if "___" in class_name:
        plant_name, disease_name = class_name.split("___", 1)
    else:
        plant_name, disease_name = class_name, "Unknown"

    plant_name = plant_name.replace("_", " ").strip()
    disease_name = disease_name.replace("_", " ").strip()
    return plant_name, disease_name


def build_class_mapping(classes):
    mapping = {}
    for idx, class_name in enumerate(classes):
        plant_name, disease_name = parse_class_name(class_name)
        is_healthy = "healthy" in disease_name.lower()
        summary = (
            f"The leaf appears healthy for {plant_name}."
            if is_healthy
            else f"Signs of {disease_name.lower()} were detected on the {plant_name.lower()} leaf."
        )
        recommended_next_step = (
            "Continue regular care, hydration, and monitoring."
            if is_healthy
            else "Isolate the affected plant, remove badly damaged leaves, and treat with the appropriate fungicide or pesticide."
        )

        mapping[str(idx)] = {
            "combined_label": class_name,
            "plant_name": plant_name,
            "disease_name": disease_name,
            "is_healthy": is_healthy,
            "summary": summary,
            "recommended_next_step": recommended_next_step,
        }
    return mapping


def save_class_mapping(mapping: Dict[str, Dict[str, object]]) -> None:
    MAPPING_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(MAPPING_PATH, "w", encoding="utf-8") as f:
        json.dump(mapping, f, indent=2, ensure_ascii=False)
    print(f"Saved class mapping to {MAPPING_PATH}")


def get_device():
    if getattr(torch.backends, "mps", None) and torch.backends.mps.is_available():
        return torch.device("mps")
    if torch.cuda.is_available():
        return torch.device("cuda")
    return torch.device("cpu")


def make_dataloaders(batch_size: int = 32, num_workers: int = 2):
    train_transform = transforms.Compose([
        transforms.RandomResizedCrop(224),
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
    ])
    val_transform = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
    ])

    train_dir = DATA_DIR / "train"
    valid_dir = DATA_DIR / "valid"

    if not train_dir.exists() or not valid_dir.exists():
        raise FileNotFoundError(
            f"Train or valid directory not found in {DATA_DIR}."
        )

    train_dataset = datasets.ImageFolder(str(train_dir), transform=train_transform)
    val_dataset = datasets.ImageFolder(str(valid_dir), transform=val_transform)

    train_loader = DataLoader(
        train_dataset,
        batch_size=batch_size,
        shuffle=True,
        num_workers=num_workers,
        pin_memory=False,
    )
    val_loader = DataLoader(
        val_dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=num_workers,
        pin_memory=False,
    )

    return train_loader, val_loader, train_dataset.classes


def build_model(num_classes: int, device: torch.device):
    try:
        model = models.efficientnet_b0(weights=models.EfficientNet_B0_Weights.DEFAULT)
    except Exception as exc:
        print(f"Warning: pretrained weights unavailable, training from scratch. ({exc})")
        model = models.efficientnet_b0(weights=None)

    num_features = model.classifier[1].in_features
    model.classifier[1] = nn.Linear(num_features, num_classes)
    model.to(device)
    return model


def set_backbone_trainable(model, trainable: bool):
    for param in model.features.parameters():
        param.requires_grad = trainable
    for param in model.classifier.parameters():
        param.requires_grad = True


def evaluate(model, loader, criterion, device):
    model.eval()
    running_loss = 0.0
    correct = 0
    total = 0

    with torch.no_grad():
        for inputs, labels in loader:
            inputs = inputs.to(device)
            labels = labels.to(device)
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            running_loss += loss.item() * inputs.size(0)
            _, preds = torch.max(outputs, 1)
            correct += (preds == labels).sum().item()
            total += labels.size(0)

    return running_loss / total, correct / total if total else 0.0


def train_one_epoch(model, loader, optimizer, criterion, device):
    model.train()
    running_loss = 0.0
    correct = 0
    total = 0

    for inputs, labels in loader:
        inputs = inputs.to(device)
        labels = labels.to(device)
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        running_loss += loss.item() * inputs.size(0)
        _, preds = torch.max(outputs, 1)
        correct += (preds == labels).sum().item()
        total += labels.size(0)

    return running_loss / total, correct / total if total else 0.0


def run_training():
    device = get_device()
    print(f"Using device: {device}")
    torch.set_num_threads(4)

    train_loader, val_loader, classes = make_dataloaders(batch_size=32, num_workers=2)
    print(f"Found {len(classes)} classes.")

    mapping = build_class_mapping(classes)
    save_class_mapping(mapping)

    model = build_model(len(classes), device)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=1e-4)

    print("Starting head-only training...")
    set_backbone_trainable(model, False)
    for epoch in range(1, 6):
        train_loss, train_acc = train_one_epoch(model, train_loader, optimizer, criterion, device)
        val_loss, val_acc = evaluate(model, val_loader, criterion, device)
        print(f"Head Epoch {epoch}: train_loss={train_loss:.4f}, train_acc={train_acc:.4f}, val_loss={val_loss:.4f}, val_acc={val_acc:.4f}")

    print("Starting full fine-tuning...")
    set_backbone_trainable(model, True)
    optimizer = optim.Adam(model.parameters(), lr=1e-5)
    for epoch in range(1, 11):
        train_loss, train_acc = train_one_epoch(model, train_loader, optimizer, criterion, device)
        val_loss, val_acc = evaluate(model, val_loader, criterion, device)
        print(f"Fine-tune Epoch {epoch}: train_loss={train_loss:.4f}, train_acc={train_acc:.4f}, val_loss={val_loss:.4f}, val_acc={val_acc:.4f}")

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    torch.save(model.state_dict(), MODEL_PATH)
    print(f"Saved trained model to {MODEL_PATH}")


if __name__ == "__main__":
    run_training()
