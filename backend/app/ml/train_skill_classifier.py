import json
from pathlib import Path

import numpy as np
import tensorflow as tf


BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "training_data.json"
MODEL_DIR = BASE_DIR / "saved_model"
MODEL_PATH = MODEL_DIR / "skill_classifier.keras"
LABELS_PATH = MODEL_DIR / "labels.json"


def load_data():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    texts = [item["text"] for item in data]
    labels = [item["label"] for item in data]
    return texts, labels


def main():
    texts, labels = load_data()

    unique_labels = sorted(list(set(labels)))
    label_to_index = {label: idx for idx, label in enumerate(unique_labels)}
    y = np.array([label_to_index[label] for label in labels], dtype=np.int32)

    vocab_size = 2000
    sequence_length = 40

    vectorizer = tf.keras.layers.TextVectorization(
        max_tokens=vocab_size,
        output_mode="int",
        output_sequence_length=sequence_length,
    )

    text_ds = tf.data.Dataset.from_tensor_slices(texts).batch(8)
    vectorizer.adapt(text_ds)

    model = tf.keras.Sequential([
        tf.keras.Input(shape=(1,), dtype=tf.string),
        vectorizer,
        tf.keras.layers.Embedding(vocab_size, 32),
        tf.keras.layers.GlobalAveragePooling1D(),
        tf.keras.layers.Dense(32, activation="relu"),
        tf.keras.layers.Dense(len(unique_labels), activation="softmax"),
    ])

    model.compile(
        optimizer="adam",
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"],
    )

    x = np.array(texts, dtype=object)

    model.fit(
        x,
        y,
        epochs=30,
        batch_size=4,
        verbose=1,
    )

    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    model.save(MODEL_PATH)

    with open(LABELS_PATH, "w", encoding="utf-8") as f:
        json.dump(
            {
                "labels": unique_labels,
                "label_to_index": label_to_index,
            },
            f,
            ensure_ascii=False,
            indent=2,
        )

    print("Training complete.")
    print(f"Saved model to: {MODEL_PATH}")
    print(f"Saved labels to: {LABELS_PATH}")


if __name__ == "__main__":
    main()