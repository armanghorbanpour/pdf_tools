<div align="center">

# PDF Tools

### A multi-purpose PDF utility web application built with Django

A lightweight, locally run web application for converting images into
PDF files, removing PDF watermarks, and converting PDF documents into
editable Word files.

[![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-Framework-092E20?logo=django&logoColor=white)](https://www.djangoproject.com/)
[![HTML5](https://img.shields.io/badge/HTML5-E34F26?logo=html5&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/HTML)
[![CSS3](https://img.shields.io/badge/CSS3-1572B6?logo=css3&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/CSS)
[![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?logo=javascript&logoColor=black)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
[![PyMuPDF](https://img.shields.io/badge/PDF%20Processing-PyMuPDF-4B8BBE)](https://pymupdf.readthedocs.io/)

</div>
------------------------------------------------------------------------

## Overview

**PDF Tools** is a small multi-purpose web application developed with
**Python and Django**. It brings together three useful document
utilities in one simple interface:

-   Convert multiple images into a single PDF document.
-   Remove watermarks from PDF files using text search or manual area
    selection.
-   Convert PDF documents into Word (`.docx`) files.

The frontend uses Django Templates, HTML, CSS, and vanilla JavaScript.
Bootstrap can be used for interface styling where needed.

The project is intended for local development, testing, and learning. It
does not include user registration, login, or account management, and it
is not currently designed as a deployed public service.

## Features

### Image to PDF

-   Select multiple images.
-   Combine the selected images into one PDF file.

### PDF Watermark Remover

The watermark removal tool provides two approaches:

#### Text Search

-   Enter the watermark text.
-   Search for matching text on PDF pages using PyMuPDF's
    `page.search_for()`.
-   Add redaction annotations to matching text rectangles.
-   Fill redacted areas with white.

#### Select Area

-   Preview PDF pages in the browser using PDF.js.
-   Select watermark areas by dragging the mouse over the page.
-   Select areas on multiple pages.
-   Send normalized selection coordinates from the frontend to Django.
-   Convert the selected coordinates into PDF page coordinates and apply
    redactions.

### PDF to Word

-   Convert a PDF document into a Word (`.docx`) file.

## Important Notes About Watermark Removal

Watermark removal depends on how the watermark is stored inside the PDF.
It may be represented as searchable text, vector paths, an image, or a
combination of these.

The current implementation uses PyMuPDF redaction:

-   **Text Search** uses `page.search_for()` and applies redactions with
    the default `page.apply_redactions()` behavior.
-   **Select Area** adds redaction annotations with a white fill and
    applies redactions using:

``` python
page.apply_redactions(
    images=0,
    graphics=2,
    text=0
)
```

Redaction is a destructive operation. If original document content
overlaps a matched or selected area, that content may also be removed.
Some watermark types may not be detected or removed correctly by the
current methods.

**Always keep an unchanged copy of the original PDF and inspect the
generated file before using it.** The application does not guarantee
perfect watermark removal or preservation of all underlying content.

## Tech Stack

  Technology         Purpose
  ------------------ ----------------------------------------------------------
  Python             Main programming language
  Django             Backend framework, URL routing, views, and file handling
  PyMuPDF (`fitz`)   PDF text search and redaction
  PDF.js             In-browser PDF preview for area selection
  HTML5              Page structure
  CSS3               Styling and layout
  JavaScript         Frontend interactions and PDF area selection
  Django Templates   Server-rendered frontend
  Bootstrap          Optional UI styling

## Project Structure

The following is a simplified view of the project structure based on the
current implementation. Additional project and configuration files may
exist.

``` text
pdf-tools/
│
├── manage.py
├── tools/
│   ├── services/
│   │   └── watermark_remover.py
│   ├── views.py
│   └── utils.py
│
├── templates/
│   └── tools/
│       └── watermark_remover.html
│
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       ├── main.js
│       └── watermark.js
│
└── media/
    └── outputs/
```

### Main project areas

-   **`tools/`** --- Django application code, including views, utility
    functions, and document-processing services.
-   **`tools/services/`** --- processing logic for PDF-related
    operations. The current watermark implementation is in
    `watermark_remover.py`.
-   **`templates/`** --- Django HTML templates.
-   **`static/`** --- frontend CSS and JavaScript files.
-   **`media/outputs/`** --- generated output files, based on the
    configured `MEDIA_ROOT`.

The exact directory layout may differ slightly depending on the local
project configuration.

## Getting Started

Follow these steps to run the project locally.

### 1. Clone the repository

``` bash
git clone https://github.com/armanghorbanpour/PDF_tools.git
cd pdf_tools
```


### 2. Create and activate a virtual environment

**Windows (PowerShell):**

``` powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**

``` cmd
python -m venv venv
venv\Scripts\activate
```

**macOS / Linux:**

``` bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

If the repository includes a `requirements.txt` file:

``` bash
pip install -r requirements.txt
```

If it does not, install the packages required by the project. Django and
PyMuPDF are used by the backend and watermark-removal service. Check the
image-to-PDF and PDF-to-Word service implementations for their
additional dependencies.

### 4. Apply database migrations

``` bash
python manage.py migrate
```

### 5. Run the development server

``` bash
python manage.py runserver
```

Open the application in your browser:

``` text
http://127.0.0.1:8000/
```

Press `Ctrl + C` in the terminal to stop the server.

## Using the Watermark Remover

### Text Search

1.  Open the watermark removal tool.
2.  Select a PDF file.
3.  Choose **Text Search**.
4.  Enter the watermark text.
5.  Start the operation.
6.  Download and inspect the generated PDF.

This method requires the watermark to be searchable as text in the PDF.
Text that appears selectable in a PDF viewer is not necessarily
searchable through PyMuPDF.

### Select Area

1.  Open the watermark removal tool.
2.  Select a PDF file.
3.  Choose **Select Area**.
4.  Wait for the PDF preview to load.
5.  Drag the mouse over the watermark area.
6.  Repeat the selection on other pages if needed.
7.  Start the operation.
8.  Download and inspect the generated PDF.

The browser preview uses PDF.js version `3.11.174` loaded from a CDN. An
internet connection is therefore required for this preview unless PDF.js
is configured to be served locally.

## Output Files

The watermark-removal service saves generated files under:

``` text
MEDIA_ROOT/outputs/
```

Output filenames are generated using the `generate_filename()` utility
from `tools.utils`.

Make sure the Django `MEDIA_ROOT` setting matches the intended output
directory. The corresponding Django views and URL configuration are
responsible for providing access to generated files.

## Limitations

-   This project is intended for local use and testing, not public
    production deployment.
-   User registration, login, and account management are not included.
-   Redaction may remove original content that overlaps a watermark or
    selected area.
-   Watermark removal is not guaranteed for every PDF structure or
    watermark type.
-   PDF-to-Word conversion may not preserve the original layout, fonts,
    spacing, or document structure exactly.
-   PDF.js is currently loaded from a CDN for browser preview.
-   The current frontend JavaScript rejects PDF files larger than 25 MB
    for preview. This is a client-side check and does not replace
    server-side file validation.
-   Keep a backup of every original document before processing it.

## Troubleshooting

### The PDF preview does not load

-   Check your internet connection because PDF.js is loaded from a CDN.
-   Open browser developer tools with `F12` and inspect the Console for
    errors.
-   Hard-refresh the page using `Ctrl + Shift + R`.

### Text Search cannot find the watermark

The watermark may be stored as vector paths or an image rather than
searchable text. Try **Select Area**, keeping in mind that removal is
not guaranteed.

### Some original content disappears after redaction

The redaction rectangle may overlap content belonging to the original
document. Restore the original PDF and try a smaller, more precise area.
Redaction cannot always distinguish a watermark from document content
underneath it.

### Frontend changes are not visible

The browser may be using cached CSS or JavaScript files. Perform a hard
refresh with `Ctrl + Shift + R`.

## Project Scope

The current version focuses on these three utilities:

-   Multiple Images to PDF
-   PDF Watermark Remover
-   PDF to Word

Authentication, user accounts, online deployment, and public-service
features are outside the scope of the current version.

## Contributing

Suggestions, bug reports, and improvements are welcome.

1.  Fork the repository.
2.  Create a feature branch.
3.  Make your changes.
4.  Test the application locally.
5.  Open a pull request with a clear description of your changes.


