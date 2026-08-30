"""
wsgi.py
Production WSGI entry point.

Usage with gunicorn (Render / Linux):
    gunicorn wsgi:app --bind 0.0.0.0:$PORT --workers 1 --timeout 120 --preload

Usage with waitress (Windows local fallback):
    python run.py
"""

import os
from app import create_app

app = create_app(os.getenv("FLASK_ENV", "production"))

