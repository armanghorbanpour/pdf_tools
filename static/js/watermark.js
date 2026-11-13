
document.addEventListener("DOMContentLoaded", function () {

    const form = document.getElementById("watermarkForm");

    if (!form) return;

    const pdfInput = document.getElementById("watermarkPdf");
    const textMode = document.getElementById("textMode");
    const areaMode = document.getElementById("areaMode");
    const preview = document.getElementById("pdfPreview");
    const areasInput = document.getElementById("areasJson");
    const submitButton = document.getElementById("watermarkSubmit");

    let selectedAreas = [];
    let pdfDocument = null;

    // PDF.js configuration
    if (typeof pdfjsLib === "undefined") {
        console.error("PDF.js library is not loaded.");
        return;
    }

    pdfjsLib.GlobalWorkerOptions.workerSrc =
        "https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js";


    // Get selected mode
    function getMode() {
        const selected = document.querySelector(
            'input[name="mode"]:checked'
        );

        return selected ? selected.value : "text";
    }


    // Switch between removal methods
    document.querySelectorAll('input[name="mode"]').forEach(radio => {

        radio.addEventListener("change", function () {

            const isArea = this.value === "area";

            textMode.style.display = isArea ? "none" : "block";
            areaMode.style.display = isArea ? "block" : "none";

            if (isArea && pdfInput.files.length && !pdfDocument) {
                loadPDF();
            }

        });

    });


    // Reset preview when file changes
    pdfInput.addEventListener("change", function () {

        pdfDocument = null;
        selectedAreas = [];

        areasInput.value = "";
        preview.innerHTML = "";

        if (getMode() === "area" && this.files.length) {
            loadPDF();
        }

    });


    // Load PDF using PDF.js
    async function loadPDF() {

        const file = pdfInput.files[0];

        if (!file) return;

        if (file.type !== "application/pdf") {
            alert("Please select a valid PDF file.");
            return;
        }

        if (file.size > 25 * 1024 * 1024) {
            alert("Maximum file size is 25 MB.");
            return;
        }

        preview.innerHTML = "<p>Loading PDF...</p>";

        try {

            const buffer = await file.arrayBuffer();

            pdfDocument = await pdfjsLib.getDocument({
                data: buffer
            }).promise;

            preview.innerHTML = "";

            for (
                let pageNumber = 1;
                pageNumber <= pdfDocument.numPages;
                pageNumber++
            ) {

                await renderPage(pageNumber);

            }

        } catch (error) {

            console.error("PDF loading error:", error);

            preview.innerHTML = "";

            alert("Could not load PDF preview.");

            pdfDocument = null;

        }

    }


    // Render each PDF page
    async function renderPage(pageNumber) {

        const page = await pdfDocument.getPage(pageNumber);

        const viewport = page.getViewport({
            scale: 1.2
        });

        const pageWrapper = document.createElement("div");

        pageWrapper.className = "pdf-page-wrapper";

        pageWrapper.style.width = viewport.width + "px";
        pageWrapper.style.maxWidth = "100%";

        const canvas = document.createElement("canvas");

        canvas.width = viewport.width;
        canvas.height = viewport.height;

        canvas.style.width = "100%";
        canvas.style.height = "auto";

        const overlay = document.createElement("div");

        overlay.className = "pdf-selection-overlay";

        overlay.dataset.page = pageNumber - 1;

        pageWrapper.appendChild(canvas);
        pageWrapper.appendChild(overlay);

        const pageTitle = document.createElement("div");

        pageTitle.className = "pdf-page-title";
        pageTitle.textContent = "Page " + pageNumber;

        preview.appendChild(pageTitle);
        preview.appendChild(pageWrapper);

        const context = canvas.getContext("2d");

        await page.render({
            canvasContext: context,
            viewport: viewport
        }).promise;

        enableSelection(overlay);

    }


    // Enable mouse selection
    function enableSelection(overlay) {

        let startX = 0;
        let startY = 0;
        let selection = null;

        // Start selection
        overlay.addEventListener("pointerdown", function (event) {

            if (event.button !== 0) return;

            event.preventDefault();

            const rect = overlay.getBoundingClientRect();

            startX = event.clientX - rect.left;
            startY = event.clientY - rect.top;

            selection = document.createElement("div");

            selection.className = "selected-watermark-area";

            selection.style.left = startX + "px";
            selection.style.top = startY + "px";

            overlay.appendChild(selection);

            overlay.setPointerCapture(event.pointerId);

        });


        // Update selection while dragging
        overlay.addEventListener("pointermove", function (event) {

            if (!selection) return;

            const rect = overlay.getBoundingClientRect();

            const currentX = event.clientX - rect.left;
            const currentY = event.clientY - rect.top;

            const left = Math.min(startX, currentX);
            const top = Math.min(startY, currentY);

            const width = Math.abs(currentX - startX);
            const height = Math.abs(currentY - startY);

            selection.style.left = left + "px";
            selection.style.top = top + "px";

            selection.style.width = width + "px";
            selection.style.height = height + "px";

        });


        // Finish selection
        function finishSelection() {

            if (!selection) return;

            const rect = overlay.getBoundingClientRect();

            const selectionRect = selection.getBoundingClientRect();

            const x = selectionRect.left - rect.left;
            const y = selectionRect.top - rect.top;

            const width = selectionRect.width;
            const height = selectionRect.height;

            if (width >= 3 && height >= 3) {

                selectedAreas.push({

                    page: Number(overlay.dataset.page),

                    x: x / rect.width,
                    y: y / rect.height,

                    width: width / rect.width,
                    height: height / rect.height

                });

                updateAreasInput();

            } else {

                selection.remove();

            }

            selection = null;

        }


        overlay.addEventListener("pointerup", finishSelection);

        overlay.addEventListener("pointercancel", finishSelection);

    }


    // Update hidden form input
    function updateAreasInput() {

        areasInput.value = JSON.stringify(selectedAreas);

        console.log("Selected areas:", selectedAreas);

    }


    // Validate before submitting
    form.addEventListener("submit", function (event) {

        if (getMode() === "area") {

            if (selectedAreas.length === 0) {

                event.preventDefault();

                alert("Please select at least one area.");

                return;

            }

            updateAreasInput();

        }

        submitButton.disabled = true;

        submitButton.textContent = "Processing...";

    });

});
