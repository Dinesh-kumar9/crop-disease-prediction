"""
tests/test_apis.py
Tests for external API integrations: Weather and Translation.

Run with:  pytest tests/test_apis.py -v
"""

import sys
import os
from pathlib import Path

# Ensure project root is on sys.path when running tests directly
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from modules import weather, translator


class TestWeatherAPI:
    """Tests for the OpenWeatherMap weather module."""

    def test_forecast_returns_dict(self):
        """get_weather_forecast must always return a dict."""
        data = weather.get_weather_forecast("Hyderabad")
        assert isinstance(data, dict), "Expected a dict response"

    def test_forecast_has_required_keys(self):
        """Response must contain 'forecast' and 'error' keys."""
        data = weather.get_weather_forecast("Hyderabad")
        assert "forecast" in data
        assert "error" in data

    def test_forecast_is_list(self):
        """forecast value must be a list (even if empty)."""
        data = weather.get_weather_forecast("Hyderabad")
        assert isinstance(data["forecast"], list)

    def test_invalid_city_returns_error(self):
        """An invalid city name should return an error message, not raise."""
        data = weather.get_weather_forecast("InvalidCityXYZ123")
        # Either 'error' is set OR mock data was returned gracefully
        if data.get("error"):
            assert isinstance(data["error"], str)
        else:
            # Mock data was used — still a valid response
            assert isinstance(data.get("forecast"), list)

    def test_risk_analysis_on_mock(self):
        """analyze_weather_risks should return a list."""
        data = weather.get_mock_weather_forecast("Hyderabad")
        risks = weather.analyze_weather_risks(data["forecast"])
        assert isinstance(risks, list)


class TestTranslatorModule:
    """Tests for the multilingual translator module."""

    def test_city_detection_hyderabad(self):
        """Hyderabad should be detected as Telugu."""
        lang = translator.detect_language_from_city("Hyderabad")
        assert lang == "te"

    def test_city_detection_chennai(self):
        """Chennai should be detected as Tamil."""
        lang = translator.detect_language_from_city("Chennai")
        assert lang == "ta"

    def test_city_detection_unknown(self):
        """Unknown city should fall back to English."""
        lang = translator.detect_language_from_city("UnknownCityXYZ")
        assert lang == "en"

    def test_translate_text_same_language(self):
        """Translating to 'en' should return original text unchanged."""
        result = translator.translate_text("Apply fungicide", "en")
        assert result == "Apply fungicide"

    def test_translate_schedule_english(self):
        """Translating to 'en' should leave schedule unchanged."""
        schedule = [{"date": "Today", "task": "Irrigate Crop", "details": "Needs water.", "icon": "💧"}]
        result = translator.translate_schedule(schedule, "en")
        assert result == schedule

    def test_language_names_populated(self):
        """LANGUAGE_NAMES must contain key entries."""
        assert "en" in translator.LANGUAGE_NAMES
        assert "te" in translator.LANGUAGE_NAMES
        assert "hi" in translator.LANGUAGE_NAMES
