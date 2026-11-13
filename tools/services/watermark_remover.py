
import os
import json
import pymupdf as fitz
from django.conf import settings
from tools.utils import generate_filename


def remove_text_watermark(pdf_file, watermark_text):

    if not watermark_text or not watermark_text.strip():
        raise ValueError("Please enter watermark text.")

    output_dir = settings.MEDIA_ROOT / 'outputs'
    os.makedirs(output_dir, exist_ok=True)

    output_filename = generate_filename('pdf')
    output_path = output_dir / output_filename

    document = None

    try:
        pdf_file.seek(0)

        document = fitz.open(
            stream=pdf_file.read(),
            filetype='pdf'
        )

        if document.is_encrypted:
            raise ValueError("Encrypted PDF is not supported.")

        matches = 0

        for page in document:

            rectangles = page.search_for(watermark_text)

            for rect in rectangles:
                page.add_redact_annot(
                    rect,
                    fill=(1, 1, 1)
                )
                matches += 1

            if rectangles:
                page.apply_redactions()

        if matches == 0:
            raise ValueError(
                "Watermark text was not found. Try Select Area mode."
            )

        document.save(
            str(output_path),
            garbage=4,
            deflate=True
        )

        return output_filename

    except Exception:
        if output_path.exists():
            output_path.unlink()
        raise

    finally:
        if document:
            document.close()


def remove_area_watermark(pdf_file, areas_json):

    output_dir = settings.MEDIA_ROOT / 'outputs'
    os.makedirs(output_dir, exist_ok=True)

    output_filename = generate_filename('pdf')
    output_path = output_dir / output_filename

    document = None

    try:

        areas = json.loads(areas_json)

        if not isinstance(areas, list) or not areas:
            raise ValueError("Please select at least one area.")

        if len(areas) > 100:
            raise ValueError("Too many selected areas.")

        pdf_file.seek(0)

        document = fitz.open(
            stream=pdf_file.read(),
            filetype='pdf'
        )

        if document.is_encrypted:
            raise ValueError("Encrypted PDF is not supported.")

        for area in areas:

            page_index = area.get('page')

            if not isinstance(page_index, int):
                raise ValueError("Invalid page number.")

            if not 0 <= page_index < len(document):
                raise ValueError("Invalid page number.")

            x = float(area.get('x', -1))
            y = float(area.get('y', -1))
            width = float(area.get('width', 0))
            height = float(area.get('height', 0))

            # Coordinates are normalized between 0 and 1.
            if not (
                0 <= x < 1 and
                0 <= y < 1 and
                0 < width <= 1 and
                0 < height <= 1 and
                x + width <= 1.000001 and
                y + height <= 1.000001
            ):
                raise ValueError("Invalid selection coordinates.")

            page = document[page_index]

            page_rect = page.rect

            rect = fitz.Rect(
                x * page_rect.width,
                y * page_rect.height,
                (x + width) * page_rect.width,
                (y + height) * page_rect.height
            )

            page.add_redact_annot(
                rect,
                fill=(1,1,1)
            )

        affected_pages = set(
            area['page'] for area in areas
        )

        for page_index in affected_pages:

            page = document[page_index]

            # Remove intersecting vector graphics.
            # Preserve embedded images.
            # Remove text inside the selected area.
            page.apply_redactions(
                images=0,
                graphics=2,
                text=0
            )

        document.save(
            str(output_path),
            garbage=4,
            deflate=True
        )

        return output_filename

    except Exception:
        if output_path.exists():
            output_path.unlink()
        raise

    finally:
        if document:
            document.close()