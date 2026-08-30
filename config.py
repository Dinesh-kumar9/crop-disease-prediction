"""
config.py
Centralised configuration for all environments.
Loads secrets from .env file via python-dotenv.
"""
import os
from pathlib import Path

# Load .env file if present
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # python-dotenv not installed; rely on OS env vars

BASE_DIR = Path(__file__).resolve().parent


class Config:
    """Base configuration shared across all environments."""

    # Flask
    SECRET_KEY: str = os.getenv("SECRET_KEY", "change-me-in-production")
    MAX_CONTENT_LENGTH: int = 16 * 1024 * 1024  # 16 MB max upload

    # Paths
    MODEL_DIR: Path = BASE_DIR / "models"
    UPLOAD_FOLDER: Path = BASE_DIR / "static" / "uploads"
    LOG_DIR: Path = BASE_DIR / "logs"

    # Model filenames
    TOMATO_MODEL_FILE: str = "tomato_multiclass_model.h5"
    BANANA_MODEL_FILE: str = "banana_multiclass_model.h5"

    # Weather API
    OWM_API_KEY: str = os.getenv("OWM_API_KEY", "")
    OWM_BASE_URL: str = "http://api.openweathermap.org/data/2.5/forecast"

    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE: str = "app.log"

    # Supported crops and class labels
    TOMATO_CLASSES: list = [
        "Early_blight",
        "Healthy",
        "Late_blight",
        "Leaf_Miner",
        "Magnesium_Deficiency",
        "Nitrogen_Deficiency",
        "Potassium_Deficiency",
        "Spotted_Wilt_Virus",
    ]

    BANANA_CLASSES: list = [
        "cordana",
        "healthy",
        "pestalotiopsis",
        "sigatoka",
    ]


class DevelopmentConfig(Config):
    """Development-specific configuration."""
    DEBUG: bool = True
    TESTING: bool = False
    LOG_LEVEL: str = "DEBUG"


class ProductionConfig(Config):
    """Production-specific configuration."""
    DEBUG: bool = False
    TESTING: bool = False
    LOG_LEVEL: str = "WARNING"


class TestingConfig(Config):
    """Testing-specific configuration."""
    DEBUG: bool = True
    TESTING: bool = True
    # Use in-memory / temp paths during tests
    UPLOAD_FOLDER: Path = BASE_DIR / "tests" / "fixtures" / "uploads"


# Map of config names to classes
config_map = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
    "default": DevelopmentConfig,
}
