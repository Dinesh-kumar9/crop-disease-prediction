"""
scripts/download_models.py
Downloads ML model files from Google Drive during Render build.

Usage:
    python scripts/download_models.py

Reads from environment variables:
    TOMATO_MODEL_ID  — Google Drive file ID for tomato model
    BANANA_MODEL_ID  — Google Drive file ID for banana model
"""

import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
MODELS_DIR = PROJECT_ROOT / "models"
MODELS_DIR.mkdir(exist_ok=True)

MODELS = {
    "tomato_multiclass_model.h5": os.getenv(
        "TOMATO_MODEL_ID", "1Cq3APxHdK3H-o_FZCpv71OWB87awuS7A"
    ),
    "banana_multiclass_model.h5": os.getenv(
        "BANANA_MODEL_ID", "1WcnYiuTRbT4OV-N4mWcktqafDZWVM2Ao"
    ),
}


def download_model(filename: str, file_id: str) -> None:
    dest = MODELS_DIR / filename

    if dest.exists():
        size_mb = dest.stat().st_size / (1024 * 1024)
        print(f"[SKIP] {filename} already exists ({size_mb:.1f} MB)")
        return

    if not file_id:
        print(f"[ERROR] No file ID provided for {filename}. "
              f"Set TOMATO_MODEL_ID / BANANA_MODEL_ID env vars.", file=sys.stderr)
        sys.exit(1)

    print(f"[DOWNLOAD] {filename} from Google Drive (id={file_id}) ...")

    try:
        import gdown
        url = f"https://drive.google.com/uc?id={file_id}"
        gdown.download(url, str(dest), quiet=False)

        if not dest.exists() or dest.stat().st_size < 1_000_000:
            print(f"[ERROR] Download failed or file too small: {dest}", file=sys.stderr)
            sys.exit(1)

        size_mb = dest.stat().st_size / (1024 * 1024)
        print(f"[OK] {filename} downloaded ({size_mb:.1f} MB)")

    except Exception as exc:
        print(f"[ERROR] Failed to download {filename}: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    print("=" * 50)
    print("Model Download Script")
    print(f"Target directory: {MODELS_DIR}")
    print("=" * 50)

    for name, fid in MODELS.items():
        download_model(name, fid)

    print("\n[DONE] All models ready.")
