import json
from pathlib import Path

import numpy as np
import tensorflow as tf


BASE_DIR = Path(__file__).resolve().parent
MODEL_DIR = BASE_DIR / "saved_model"
MODEL_PATH = MODEL_DIR / "skill_classifier.keras"
LABELS_PATH = MODEL_DIR / "labels.json"


def load_assets():
    model = tf.keras.models.load_model(MODEL_PATH)

    with open(LABELS_PATH, "r", encoding="utf-8") as f:
        label_data = json.load(f)

    labels = label_data["labels"]
    return model, labels


def predict(text: str):
    model, labels = load_assets()

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


if __name__ == "__main__":
    result = predict("Built backend APIs with FastAPI and Python.")
    print(result)