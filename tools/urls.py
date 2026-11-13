
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path(
        'image-to-pdf/',
        views.image_to_pdf_view,
        name='image_to_pdf'
    ),

    path(
        'remove-watermark/',
        views.watermark_remover_view,
        name='watermark_remover'
    ),

    path(
        'pdf-to-word/',
        views.pdf_to_word_view,
        name='pdf_to_word'
    ),

    path(
        'download/<str:filename>/',
        views.download_file,
        name='download_file'
    ),
]
