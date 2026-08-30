"""
app/services/pipeline.py
Full analysis pipeline — orchestrates all modules for a single crop image.

Extracted from the inline logic in the original app.py (lines 160-254).
Calling run_analysis() is the single entry point for all AI and data features.
"""

import logging
from pathlib import Path
from typing import Any

from flask import current_app

from app.services.prediction import predict_disease
from app.utils.image import preprocess_image
from modules import weather, scheduler, growth_stage, translator, economics, advisor

logger = logging.getLogger(__name__)

# Crops that have a trained model (others handled gracefully)
SUPPORTED_CROPS = {"tomato", "banana"}


def run_analysis(crop: str, filepath: str | Path, city: str) -> dict[str, Any]:
    """
    Run the full crop-health analysis pipeline.

    Args:
        crop: Crop type string, e.g. 'tomato', 'banana'.
        filepath: Absolute path to the saved uploaded image.
        city: User-supplied city name for weather lookups.

    Returns:
        Dict containing all data needed to render dashboard.html.
        Raises ValueError for unsupported crops.
    """
    crop = crop.lower().strip()
    city = city.strip() or "Hyderabad"

    if crop not in SUPPORTED_CROPS:
        raise ValueError(
            f"Crop '{crop}' is not yet supported. Available: {', '.join(SUPPORTED_CROPS)}."
        )

    # --- Step 1: Image Pre-processing ---
    img_array = preprocess_image(filepath)

    # --- Step 2: Disease Detection ---
    disease, confidence = predict_disease(crop, img_array)

    # Decide effective disease label (uncertain below threshold)
    effective_disease = disease if confidence > 70 else "Uncertain"

    # --- Step 3: Growth Stage Detection (mock until real model trained) ---
    stage, stage_conf = growth_stage.predict_growth_stage(img_array)
    logger.debug("Growth stage: %s (%.2f%%)", stage, stage_conf)

    # --- Step 4: Weather Forecast ---
    weather_data = weather.get_weather_forecast(city)
    forecast = weather_data.get("forecast", [])
    weather_error = weather_data.get("error")

    risks = []
    if not weather_error and forecast:
        risks = weather.analyze_weather_risks(forecast)

    # --- Step 5: Smart Farming Schedule ---
    if weather_error or not forecast:
        logger.warning("Weather unavailable (%s). Using fallback schedule.", weather_error)
        schedule = _fallback_schedule(stage, disease, confidence)
    else:
        schedule = scheduler.get_farming_schedule(
            crop_stage=stage,
            disease_status=effective_disease,
            weather_forecast=forecast,
        )

    # --- Step 6: Economic Intelligence ---
    market_data = economics.get_market_data(crop, city)
    economic_analysis = economics.calculate_economics(crop, disease, market_data)
    economic_advice = economics.get_economic_advice(economic_analysis)

    # --- Step 7: Language Detection & Translation ---
    detected_lang = translator.detect_language_from_city(city)
    lang_name = translator.LANGUAGE_NAMES.get(detected_lang, "English")

    # --- Step 8: Multilingual Advisory ---
    recommendations = advisor.get_recommendations(disease, detected_lang)

    # Translate schedule if not English
    if detected_lang != "en":
        schedule = translator.translate_schedule(schedule, detected_lang)

    logger.info(
        "Pipeline complete | crop=%s disease=%s conf=%.2f city=%s lang=%s",
        crop, disease, confidence, city, detected_lang,
    )

    return {
        "disease": effective_disease,
        "raw_disease": disease,
        "confidence": confidence,
        "stage": stage,
        "stage_conf": stage_conf,
        "forecast": forecast,
        "weather_error": weather_error,
        "risks": risks,
        "schedule": schedule,
        "language": detected_lang,
        "language_name": lang_name,
        "city": city,
        "economics": economic_analysis,
        "economic_advice": economic_advice,
        "recommendations": recommendations,
    }


def _fallback_schedule(stage: str, disease: str, confidence: float) -> list[dict]:
    """Return a minimal schedule when weather data is unavailable."""
    schedule = [
        {
            "date": "Today",
            "task": "Monitor Crop",
            "details": f"Crop is in {stage} stage. Regular monitoring recommended.",
            "icon": "👁️",
        }
    ]
    if disease not in ("Healthy", "healthy", "Uncertain") and confidence > 70:
        schedule.insert(
            0,
            {
                "date": "Today",
                "task": f"Address {disease.replace('_', ' ')}",
                "details": "Consult an agricultural expert for treatment.",
                "icon": "⚠️",
            },
        )
    return schedule
