"""
app/__init__.py
Flask application factory.

Usage:
    from app import create_app
    app = create_app("development")
"""

import logging
import os
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path

from flask import Flask

from config import config_map


def _configure_logging(app: Flask) -> None:
    """Set up rotating file handler + stream handler for the Flask app."""
    log_dir: Path = app.config["LOG_DIR"]
    log_dir.mkdir(parents=True, exist_ok=True)

    log_level = getattr(logging, app.config["LOG_LEVEL"].upper(), logging.INFO)

    formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Rotating file handler — new file every day, keep 14 days
    file_handler = TimedRotatingFileHandler(
        log_dir / app.config["LOG_FILE"],
        when="midnight",
        backupCount=14,
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(log_level)

    # Console handler
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    stream_handler.setLevel(log_level)

    app.logger.setLevel(log_level)
    app.logger.addHandler(file_handler)
    app.logger.addHandler(stream_handler)


def _load_models(app: Flask) -> None:
    """
    Load ML models once at application startup and store them in app.extensions.
    This avoids reloading on every request.
    """
    import os
    os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
    os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
    os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

    import tensorflow as tf

    model_dir: Path = app.config["MODEL_DIR"]
    models = {}

    # Load Tomato model
    tomato_path = model_dir / app.config["TOMATO_MODEL_FILE"]
    if tomato_path.exists():
        try:
            models["tomato"] = tf.keras.models.load_model(str(tomato_path))
            app.logger.info("Tomato model loaded from %s", tomato_path)
        except Exception as exc:
            app.logger.error("Failed to load Tomato model: %s", exc)
            models["tomato"] = None
    else:
        app.logger.warning("Tomato model not found at %s", tomato_path)
        models["tomato"] = None

    # Load Banana model
    banana_path = model_dir / app.config["BANANA_MODEL_FILE"]
    if banana_path.exists():
        try:
            models["banana"] = tf.keras.models.load_model(str(banana_path))
            app.logger.info("Banana model loaded from %s", banana_path)
        except Exception as exc:
            app.logger.error("Failed to load Banana model: %s", exc)
            models["banana"] = None
    else:
        app.logger.warning("Banana model not found at %s", banana_path)
        models["banana"] = None

    app.extensions["models"] = models


def create_app(config_name: str = "default") -> Flask:
    """
    Flask application factory.

    Args:
        config_name: One of 'development', 'production', 'testing', 'default'.

    Returns:
        Configured Flask application instance.
    """
    app = Flask(
        __name__,
        template_folder="../templates",
        static_folder="../static",
    )

    # Load configuration
    cfg_class = config_map.get(config_name, config_map["default"])
    app.config.from_object(cfg_class)

    # Ensure upload folder exists
    upload_folder: Path = app.config["UPLOAD_FOLDER"]
    upload_folder.mkdir(parents=True, exist_ok=True)

    # Configure logging
    _configure_logging(app)

    # Load ML models
    _load_models(app)

    # Register blueprints
    from app.routes.main import main_bp
    app.register_blueprint(main_bp)

    app.logger.info("Application started in '%s' mode.", config_name)
    return app
