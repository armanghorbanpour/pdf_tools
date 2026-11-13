
import os
import img2pdf

from PIL import Image, ImageOps
from django.conf import settings

from tools.utils import generate_filename


ALLOWED_IMAGE_TYPES = {
    'image/jpeg',
    'image/png',
    'image/webp',
}


def convert_images_to_pdf(files):

    if not files:
        raise ValueError("Please select at least one image.")

    if len(files) > 20:
        raise ValueError("Maximum 20 images are allowed.")

    upload_dir = settings.MEDIA_ROOT / 'uploads'
    output_dir = settings.MEDIA_ROOT / 'outputs'

    os.makedirs(upload_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)

    image_paths = []
    output_path = None

    try:
        for file in files:

            if file.content_type not in ALLOWED_IMAGE_TYPES:
                raise ValueError("Unsupported image format.")

            file.seek(0)

            image = Image.open(file)
            image.verify()

            file.seek(0)

            image = Image.open(file)
            image = ImageOps.exif_transpose(image)
            image = image.convert('RGB')

            filename = generate_filename('jpg')
            image_path = upload_dir / filename

            image.save(
                image_path,
                format='JPEG',
                quality=95
            )

            image_paths.append(str(image_path))

        output_filename = generate_filename('pdf')
        output_path = output_dir / output_filename

        with open(output_path, 'wb') as output_file:
            output_file.write(
                img2pdf.convert(image_paths)
            )

        return output_filename

    except Exception:
        if output_path and output_path.exists():
            output_path.unlink()
        raise

    finally:
        for image_path in image_paths:
            try:
                os.remove(image_path)
            except OSError:
                pass
