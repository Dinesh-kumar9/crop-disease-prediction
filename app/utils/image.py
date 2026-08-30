"""
app/utils/image.py
Image pre-processing helpers for ML inference and file upload handling.
"""

import uuid
from pathlib import Path

import numpy as np
from tensorflow.keras.preprocessing import image as keras_image


def preprocess_image(filepath: str | Path, target_size: tuple = (224, 224)) -> np.ndarray:
    """
    Load and pre-process an image file for model inference.

    Args:
        filepath: Absolute path to the image file.
        target_size: (height, width) to resize the image to.

    Returns:
        numpy array of shape (1, H, W, 3) normalised to [0, 1].
    """
    img = keras_image.load_img(str(filepath), target_size=target_size)
    img_array = keras_image.img_to_array(img) / 255.0
    return np.expand_dims(img_array, axis=0)


def save_upload(file, upload_folder: str | Path) -> tuple[str, Path]:
    """
    Save a werkzeug FileStorage object to the upload folder with a
    UUID-prefixed filename to avoid collisions.

    Args:
        file: werkzeug FileStorage object (from request.files).
        upload_folder: Directory where the file should be saved.

    Returns:
        Tuple of (safe_filename, absolute_filepath).
    """
    upload_folder = Path(upload_folder)
    upload_folder.mkdir(parents=True, exist_ok=True)

    # Preserve original extension; prepend UUID to prevent name collisions
    original_name = Path(file.filename)
    safe_name = f"{uuid.uuid4().hex}{original_name.suffix.lower()}"
    filepath = upload_folder / safe_name

    file.save(str(filepath))
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
