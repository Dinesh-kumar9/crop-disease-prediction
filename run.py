"""
run.py
Development runner — launches Flask with debug mode enabled.

Usage:
    python run.py

For production, use wsgi.py with waitress instead.
"""

import webbrowser
import os

from app import create_app

app = create_app("development")

if __name__ == "__main__":
    # Open browser only on the main process, not the reloader child
    if os.environ.get("WERKZEUG_RUN_MAIN") != "true":
        webbrowser.open_new("http://127.0.0.1:5000")
    app.run(host="127.0.0.1", port=5000, debug=True)
