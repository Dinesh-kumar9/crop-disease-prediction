"""
app/utils/image.py
Image pre-processing helpers for ML inference and file upload handling.
Optimized for low-memory cloud environments.
"""

import uuid
from pathlib import Path

import numpy as np
from PIL import Image


def preprocess_image(filepath: str | Path, target_size: tuple = (224, 224)) -> np.ndarray:
    """
    Load and pre-process an image file for model inference using Pillow.
    Memory-efficient: cleanly closes the file handle after reading.

    Args:
        filepath: Absolute path to the image file.
        target_size: (height, width) to resize the image to.

    Returns:
        numpy array of shape (1, H, W, 3) normalised to [0, 1].
    """
    with Image.open(str(filepath)) as img:
        img = img.convert("RGB")
        img = img.resize(target_size, Image.Resampling.BILINEAR)
        img_array = np.asarray(img, dtype=np.float32) / 255.0
        return np.expand_dims(img_array, axis=0)


def save_upload(file, upload_folder: str | Path, max_dimension: int = 1024) -> tuple[str, Path]:
    """
    Save a werkzeug FileStorage object to the upload folder with a
    UUID-prefixed filename. Automatically rescales large mobile photos
    to max_dimension to preserve memory and disk space.

    Args:
        file: werkzeug FileStorage object (from request.files).
        upload_folder: Directory where the file should be saved.
        max_dimension: Max width/height to resize large mobile photos.

    Returns:
        Tuple of (safe_filename, absolute_filepath).
    """
    upload_folder = Path(upload_folder)
    upload_folder.mkdir(parents=True, exist_ok=True)

    safe_name = f"{uuid.uuid4().hex}.jpg"
    filepath = upload_folder / safe_name

    # Open image stream directly and downscale to prevent huge bitmap memory usage
    with Image.open(file.stream) as img:
        img = img.convert("RGB")
        img.thumbnail((max_dimension, max_dimension), Image.Resampling.LANCZOS)
        img.save(str(filepath), format="JPEG", quality=85, optimize=True)

    return safe_name, filepath


def allowed_file(filename: str, allowed_extensions: set = None) -> bool:
    """
    Check whether the uploaded filename has an allowed image extension.

    Args:
        filename: Original filename from the upload.
        allowed_extensions: Set of lowercase extensions (e.g. {'jpg', 'jpeg', 'png'}).

    Returns:
        True if the file extension is in the allowed set, False otherwise.
    """
    if allowed_extensions is None:
        allowed_extensions = {"jpg", "jpeg", "png", "webp", "bmp"}
    return "." in filename and filename.rsplit(".", 1)[1].lower() in allowed_extensions

