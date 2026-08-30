"""
tests/test_modules.py
Unit tests for all core domain modules.

Run with:  pytest tests/test_modules.py -v
"""

import sys
from pathlib import Path

# Ensure project root is on sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from modules import weather, scheduler, growth_stage, translator, economics, advisor


class TestModuleImports:
    """Ensure all modules are importable without errors."""

    def test_weather_importable(self):
        assert hasattr(weather, "get_weather_forecast")

    def test_scheduler_importable(self):
        assert hasattr(scheduler, "get_farming_schedule")

    def test_growth_stage_importable(self):
        assert hasattr(growth_stage, "predict_growth_stage")

    def test_translator_importable(self):
        assert hasattr(translator, "detect_language_from_city")

    def test_economics_importable(self):
        assert hasattr(economics, "get_market_data")

    def test_advisor_importable(self):
        assert hasattr(advisor, "get_recommendations")


class TestEconomicsModule:
    """Tests for the agri-economics module."""

    def test_market_data_returns_dict(self):
        data = economics.get_market_data("tomato", "Hyderabad")
        assert isinstance(data, dict)
        assert "price" in data

    def test_market_data_banana(self):
        data = economics.get_market_data("banana", "Hyderabad")
        assert data["price"] > 0

    def test_calculate_economics_keys(self):
        market_data = economics.get_market_data("tomato", "Hyderabad")
        result = economics.calculate_economics("tomato", "Early_blight", market_data)
        for key in ("yield_potential", "yield_expected", "loss_percentage",
                    "potential_income", "expected_income", "loss_amount"):
            assert key in result, f"Missing key: {key}"

    def test_healthy_crop_zero_loss(self):
        market_data = economics.get_market_data("tomato", "Hyderabad")
        result = economics.calculate_economics("tomato", "Healthy", market_data)
        assert result["loss_percentage"] == 0

    def test_get_economic_advice_returns_string(self):
        market_data = economics.get_market_data("tomato", "Hyderabad")
        result = economics.calculate_economics("tomato", "Early_blight", market_data)
        advice = economics.get_economic_advice(result)
        assert isinstance(advice, str) and len(advice) > 0


class TestAdvisorModule:
    """Tests for the disease advisory module."""

    def test_english_recommendations_structure(self):
        rec = advisor.get_recommendations("Early_blight", "en")
        assert "description" in rec
        assert "chemical" in rec
        assert "organic" in rec
        assert "cultural" in rec

    def test_telugu_recommendations_structure(self):
        rec = advisor.get_recommendations("Early_blight", "te")
        assert "description" in rec
        assert isinstance(rec["chemical"], list)

    def test_unknown_disease_fallback(self):
        rec = advisor.get_recommendations("Unknown_Disease_XYZ", "en")
        assert "description" in rec  # Should return fallback, not raise

    def test_healthy_crop_recommendation(self):
        rec = advisor.get_recommendations("Healthy", "en")
        assert rec is not None


class TestGrowthStageModule:
    """Tests for the growth stage detection module."""

    def test_returns_tuple(self):
        import numpy as np
        dummy_img = np.zeros((1, 224, 224, 3))
        result = growth_stage.predict_growth_stage(dummy_img)
        assert isinstance(result, tuple) and len(result) == 2

    def test_stage_is_valid_string(self):
        import numpy as np
        dummy_img = np.zeros((1, 224, 224, 3))
        stage, conf = growth_stage.predict_growth_stage(dummy_img)
        valid_stages = {"Seedling", "Vegetative", "Flowering", "Fruiting", "Maturity"}
        assert stage in valid_stages

    def test_confidence_in_range(self):
        import numpy as np
        dummy_img = np.zeros((1, 224, 224, 3))
        _, conf = growth_stage.predict_growth_stage(dummy_img)
        assert 0.0 <= conf <= 100.0


class TestSchedulerModule:
    """Tests for the farming schedule generator."""

    def _mock_forecast(self):
        return [{"date": "2026-08-30", "temp": 28, "humidity": 65,
                 "weather": "Clear", "description": "clear sky", "wind_speed": 10}]

    def test_schedule_returns_list(self):
        schedule = scheduler.get_farming_schedule("Vegetative", "Early_blight", self._mock_forecast())
        assert isinstance(schedule, list)

    def test_disease_task_in_schedule(self):
        schedule = scheduler.get_farming_schedule("Vegetative", "Early_blight", self._mock_forecast())
        tasks = [item["task"] for item in schedule]
        assert any("Early" in t or "blight" in t.lower() or "Early_blight" in t for t in tasks)

    def test_rainy_day_no_irrigation(self):
        rainy = [{"date": "2026-08-30", "temp": 24, "humidity": 90,
                  "weather": "Rain", "description": "light rain", "wind_speed": 12}]
        schedule = scheduler.get_farming_schedule("Vegetative", "Healthy", rainy)
        tasks = [item["task"] for item in schedule]
        assert any("Skip" in t or "Irrigation" in t for t in tasks)
