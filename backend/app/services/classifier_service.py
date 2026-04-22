import json
from pathlib import Path

import numpy as np
import tensorflow as tf


BASE_DIR = Path(__file__).resolve().parent.parent / "ml"
MODEL_DIR = BASE_DIR / "saved_model"
MODEL_PATH = MODEL_DIR / "skill_classifier.keras"
LABELS_PATH = MODEL_DIR / "labels.json"

_model = None
_labels = None


def load_classifier_assets():
    global _model, _labels

    if _model is None:
        _model = tf.keras.models.load_model(MODEL_PATH)

    if _labels is None:
        with open(LABELS_PATH, "r", encoding="utf-8") as f:
            label_data = json.load(f)
        _labels = label_data["labels"]

    return _model, _labels


def predict_skill_category(text: str):
    model, labels = load_classifier_assets()

    x = np.array([text], dtype=object)
    probs = model.predict(x, verbose=0)[0]
    best_idx = int(np.argmax(probs))

    return {
        "label": labels[best_idx],
        "confidence": float(probs[best_idx]),
        "probabilities": {
            labels[i]: float(probs[i]) for i in range(len(labels))
        }
    }