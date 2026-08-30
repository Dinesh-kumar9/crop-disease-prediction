"""
app/routes/main.py
Main blueprint: handles the index page (GET) and image upload/analysis (POST).

All business logic is delegated to app.services.pipeline.run_analysis().
This file only handles HTTP concerns: validation, response rendering, error handling.
"""

import logging
from pathlib import Path

from flask import (
    Blueprint,
    current_app,
    render_template,
    request,
)

from app.services.pipeline import run_analysis, SUPPORTED_CROPS
from app.utils.image import save_upload, allowed_file

logger = logging.getLogger(__name__)

main_bp = Blueprint("main", __name__)


@main_bp.route("/", methods=["GET", "POST"])
def index():
    """
    GET  /  — Render the upload/selection form.
    POST /  — Accept crop type, city, and image; run analysis; render dashboard.
    """
    if request.method == "GET":
        return render_template("index.html")

    # ---- POST: validate inputs ----
    crop = (request.form.get("crop") or "").strip().lower()
    city = (request.form.get("city") or "Hyderabad").strip() or "Hyderabad"
    file = request.files.get("image")

    # Validate crop selection
    if crop not in SUPPORTED_CROPS:
        logger.info("Unsupported crop requested: '%s'", crop)
        return render_template(
            "index.html",
            error=True,
            en_title="Model Under Development",
            en_message=(
                f"The {crop.capitalize()} crop module is currently under development.\n\n"
                "Please select Tomato or Banana."
            ),
            te_title="మోడల్ అభివృద్ధిలో ఉంది",
            te_message=(
                f"{crop.capitalize()} పంట మోడల్ ప్రస్తుతం అభివృద్ధిలో ఉంది.\n\n"
                "ప్రస్తుతం టమాటా లేదా అరటి పంటను మాత్రమే ఎంచుకోండి."
            ),
        )

    # Validate file presence and extension
    if not file or file.filename == "":
        return render_template("index.html", error=True,
                               en_title="No File Selected",
                               en_message="Please upload a leaf image to analyse.")

    if not allowed_file(file.filename):
        return render_template("index.html", error=True,
                               en_title="Invalid File Type",
                               en_message="Accepted formats: JPG, JPEG, PNG, WEBP, BMP.")

    # ---- Save upload ----
    upload_folder: Path = current_app.config["UPLOAD_FOLDER"]
    safe_name, filepath = save_upload(file, upload_folder)
    logger.info("Image saved: %s (crop=%s, city=%s)", safe_name, crop, city)

    # ---- Run analysis pipeline ----
    try:
        result = run_analysis(crop=crop, filepath=filepath, city=city)
    except Exception as exc:
        logger.exception("Pipeline error for crop='%s': %s", crop, exc)
        return render_template(
            "index.html",
            error=True,
            en_title="Analysis Failed",
            en_message=f"An unexpected error occurred: {exc}\n\nPlease try again.",
        )

    # ---- Render dashboard ----
    # url_for('static', filename=X) maps to /static/X
    # Files are saved in static/uploads/ so we prefix accordingly
    return render_template(
        "dashboard.html",
        filename=f"uploads/{safe_name}",
        **result,
    )
