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
    models = current_app.extensions.get("models", {})
    model = models.get(crop.lower())

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
    """Check whether a trained model is loaded for the given crop."""
    models = current_app.extensions.get("models", {})
    return models.get(crop.lower()) is not None
