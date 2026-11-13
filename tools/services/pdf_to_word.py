
import os

from django.conf import settings
from pdf2docx import Converter

from tools.utils import generate_filename


def convert_pdf_to_word(pdf_file):

    upload_dir = settings.MEDIA_ROOT / 'uploads'
    output_dir = settings.MEDIA_ROOT / 'outputs'

    os.makedirs(upload_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)

    input_filename = generate_filename('pdf')
    output_filename = generate_filename('docx')

    input_path = upload_dir / input_filename
    output_path = output_dir / output_filename

    converter = None

    try:
        pdf_file.seek(0)

        with open(input_path, 'wb') as f:
            for chunk in pdf_file.chunks():
                f.write(chunk)

        converter = Converter(str(input_path))

        converter.convert(
            str(output_path),
            start=0,
            end=None
        )

        return output_filename

    except Exception:
        if output_path.exists():
            output_path.unlink()
        raise

    finally:
        if converter:
            converter.close()

        if input_path.exists():
            input_path.unlink()
