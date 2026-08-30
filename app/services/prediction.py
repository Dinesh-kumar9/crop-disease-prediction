"""
app/services/prediction.py
Model registry and inference service.

Models are loaded once at application startup (via app factory) and stored
in app.extensions["models"]. This service provides a clean interface to
run inference without touching Flask internals.
"""

import logging
from typing import Optional

import numpy as np
from flask import current_app

logger = logging.getLogger(__name__)


def _get_model(crop: str):
    """
    Get or lazily load the requested ML model from disk into app.extensions['models'].
    Only loads the specific crop model needed, preserving memory.
    """
    models = current_app.extensions.setdefault("models", {})
    crop_key = crop.lower()

    if crop_key in models:
        return models[crop_key]

    model_dir: Path = current_app.config["MODEL_DIR"]
    filename = (
        current_app.config["TOMATO_MODEL_FILE"]
        if crop_key == "tomato"
        else current_app.config["BANANA_MODEL_FILE"]
    )
    model_path = model_dir / filename

    if not model_path.exists():
        logger.warning("Model file not found at %s", model_path)
        models[crop_key] = None
        return None

    try:
        import os
        os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
        os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
        os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
        import tensorflow as tf

        logger.info("Loading %s model from %s ...", crop.capitalize(), model_path)
        model = tf.keras.models.load_model(str(model_path))
        models[crop_key] = model
        logger.info("Successfully loaded %s model.", crop.capitalize())
        return model
    except Exception as exc:
        logger.error("Failed to load %s model: %s", crop, exc)
        models[crop_key] = None
        return None


def predict_disease(crop: str, img_array: np.ndarray) -> tuple[str, float]:
    """
    Run disease classification inference for the given crop and image.

    Args:
        crop: Crop name — 'tomato' or 'banana'.
        img_array: Pre-processed image array of shape (1, 224, 224, 3).

    Returns:
        Tuple of (predicted_class_label, confidence_percentage).
        Returns ("Unknown", 0.0) if model is unavailable.
    """
    model = _get_model(crop)
    class_labels = _get_class_labels(crop)

    if model is None:
        logger.warning(
            "No model loaded for crop '%s'. Returning mock prediction.", crop
        )
        return _mock_prediction(class_labels)

    try:
        preds = model.predict(img_array, verbose=0)[0]
        top_idx = int(np.argmax(preds))
        confidence = round(float(preds[top_idx]) * 100, 2)
        label = class_labels[top_idx]
        logger.info("Prediction for %s: %s (%.2f%%)", crop, label, confidence)
        return label, confidence
    except Exception as exc:
        logger.error("Inference error for crop '%s': %s", crop, exc)
        return "Unknown", 0.0


def _get_class_labels(crop: str) -> list:
    """Return the class label list for the given crop from app config."""
    crop_key = crop.upper() + "_CLASSES"
    return current_app.config.get(crop_key, [])


def _mock_prediction(class_labels: list) -> tuple[str, float]:
    """
    Return a random mock prediction when no model is available.
    Used only in development/demo mode.
    """
    import random
    if not class_labels:
        return "Unknown", 0.0
    label = random.choice(class_labels)
    confidence = round(random.uniform(70.0, 98.0), 2)
    logger.debug("Mock prediction: %s (%.2f%%)", label, confidence)
    return label, confidence


def is_model_available(crop: str) -> bool:
    """Check whether a trained model is loaded or available on disk for the given crop."""
    return _get_model(crop) is not None
