
import os

from django.shortcuts import render
from django.http import FileResponse, Http404
from django.core.exceptions import ValidationError
from django.conf import settings
from django.contrib import messages

from .utils import (
    validate_pdf,
    validate_file_size,
    cleanup_old_files,
    get_media_path,
)
from .services.watermark_remover import (
    remove_text_watermark,
    remove_area_watermark
)
from .services.image_to_pdf import convert_images_to_pdf
from .services.pdf_to_word import convert_pdf_to_word


def home(request):
    return render(request, 'home.html')


def image_to_pdf_view(request):

    if request.method == 'POST':

        cleanup_old_files()

        try:
            files = request.FILES.getlist('images')

            if not files:
                raise ValueError("Please select images.")

            for file in files:
                validate_file_size(file)

            filename = convert_images_to_pdf(files)

            return render(
                request,
                'tools/image_to_pdf.html',
                {'output_file': filename}
            )

        except (ValueError, ValidationError) as error:
            messages.error(request, str(error))

        except Exception:
            messages.error(
                request,
                "An error occurred while converting images."
            )

    return render(request, 'tools/image_to_pdf.html')


def watermark_remover_view(request):

    if request.method == 'POST':

        cleanup_old_files()

        try:
            pdf_file = request.FILES.get('pdf_file')

            if not pdf_file:
                raise ValueError("Please upload a PDF file.")

            validate_pdf(pdf_file)

            mode = request.POST.get('mode', 'text')

            if mode == 'text':

                watermark_text = request.POST.get(
                    'watermark_text', ''
                )

                filename = remove_text_watermark(
                    pdf_file,
                    watermark_text
                )

            elif mode == 'area':

                areas_json = request.POST.get(
                    'areas_json', ''
                )

                filename = remove_area_watermark(
                    pdf_file,
                    areas_json
                )

            else:
                raise ValueError("Invalid removal method.")

            return render(
                request,
                'tools/watermark_remover.html',
                {'output_file': filename}
            )

        except (ValueError, ValidationError) as error:
            messages.error(request, str(error))

        except Exception:
            messages.error(
                request,
                "An error occurred while removing watermark."
            )

    return render(
        request,
        'tools/watermark_remover.html'
    )


def pdf_to_word_view(request):

    if request.method == 'POST':

        cleanup_old_files()

        try:
            pdf_file = request.FILES.get('pdf_file')

            if not pdf_file:
                raise ValueError("Please upload a PDF file.")

            validate_pdf(pdf_file)

            filename = convert_pdf_to_word(pdf_file)

            return render(
                request,
                'tools/pdf_to_word.html',
                {'output_file': filename}
            )

        except (ValueError, ValidationError) as error:
            messages.error(request, str(error))

        except Exception:
            messages.error(
                request,
                "An error occurred while converting PDF to Word."
            )

    return render(request, 'tools/pdf_to_word.html')


def download_file(request, filename):

    if not filename or os.path.basename(filename) != filename:
        raise Http404("File not found.")

    if not filename.endswith(('.pdf', '.docx')):
        raise Http404("File not found.")

    output_dir = settings.MEDIA_ROOT / 'outputs'
    file_path = output_dir / filename

    if not file_path.is_file():
        raise Http404("File not found.")

    content_type = (
        'application/pdf'
        if filename.endswith('.pdf')
        else 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    )

    return FileResponse(
        open(file_path, 'rb'),
        as_attachment=True,
        filename=filename,
        content_type=content_type
    )
