"""
wsgi.py
Production WSGI entry point.

Usage with waitress (Windows):
    waitress-serve --host=0.0.0.0 --port=5000 wsgi:app

Usage with gunicorn (Linux/Mac):
    gunicorn wsgi:app --bind 0.0.0.0:5000 --workers 2
"""

from app import create_app

app = create_app("production")
