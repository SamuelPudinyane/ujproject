import os
from pathlib import Path
import sys


BASE_DIR = Path(__file__).resolve().parent.parent

MEDIA_ROOT = os.path.join(BASE_DIR, "project_UJ", "static", "uploads")
UPLOAD_FOLDER = os.path.join(MEDIA_ROOT, "uploads")

def config(app):
    app.config.from_mapping(
        UPLOAD_FOLDER=UPLOAD_FOLDER
    )

# Remove placeholder path modification that breaks imports
