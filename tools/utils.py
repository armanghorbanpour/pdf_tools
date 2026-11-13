
import os
import time
import uuid

from django.conf import settings
from django.core.exceptions import ValidationError


def generate_filename(extension):
    """Generate a unique filename."""
    return f"{uuid.uuid4().hex}.{extension}"


def validate_file_size(file):
    """Check maximum upload size."""

    if file.size > settings.MAX_UPLOAD_SIZE:
        raise ValidationError(
            "File size must be less than 25 MB."
        )


def validate_pdf(file):
    """Validate PDF file signature."""

    validate_file_size(file)

    file.seek(0)
    header = file.read(5)
    file.seek(0)

    if header != b'%PDF-':
        raise ValidationError("Invalid PDF file.")


def cleanup_old_files():
    """Remove temporary files older than retention period."""

    folders = [
        settings.MEDIA_ROOT / 'uploads',
        settings.MEDIA_ROOT / 'outputs',
    ]

    retention_seconds = (
        settings.FILE_RETENTION_HOURS * 60 * 60
    )

    now = time.time()

    for folder in folders:
        os.makedirs(folder, exist_ok=True)

        for filename in os.listdir(folder):
            file_path = folder / filename

            if not os.path.isfile(file_path):
                continue

            if now - os.path.getmtime(file_path) > retention_seconds:
                try:
                    os.remove(file_path)
                except OSError:
                    pass


def get_media_path(folder, filename):
    """Build a media path."""

    return settings.MEDIA_ROOT / folder / filename
