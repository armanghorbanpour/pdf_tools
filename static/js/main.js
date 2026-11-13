
document.addEventListener("DOMContentLoaded", function () {

    const fileInput = document.getElementById("fileInput");
    const browseButton = document.getElementById("browseButton");
    const dropArea = document.getElementById("dropArea");
    const fileList = document.getElementById("fileList");
    const submitButton = document.getElementById("submitButton");

    if (!fileInput || !fileList) return;

    let selectedFiles = [];

    const allowedTypes = [
        "image/jpeg",
        "image/png",
        "image/webp"
    ];

    function updateInput() {

        const dataTransfer = new DataTransfer();

        selectedFiles.forEach(file => {
            dataTransfer.items.add(file);
        });

        fileInput.files = dataTransfer.files;

        renderFiles();
    }

    function renderFiles() {

        fileList.innerHTML = "";

        selectedFiles.forEach((file, index) => {

            const item = document.createElement("div");
            item.className = "file-item";

            const name = document.createElement("span");
            name.textContent = `${index + 1}. ${file.name}`;

            const actions = document.createElement("div");
            actions.className = "file-actions";

            const up = document.createElement("button");
            up.type = "button";
            up.className = "btn btn-sm btn-outline-secondary";
            up.textContent = "↑";
            up.disabled = index === 0;

            up.addEventListener("click", function () {
                [selectedFiles[index - 1], selectedFiles[index]] =
                    [selectedFiles[index], selectedFiles[index - 1]];

                updateInput();
            });

            const down = document.createElement("button");
            down.type = "button";
            down.className = "btn btn-sm btn-outline-secondary";
            down.textContent = "↓";
            down.disabled = index === selectedFiles.length - 1;

            down.addEventListener("click", function () {
                [selectedFiles[index], selectedFiles[index + 1]] =
                    [selectedFiles[index + 1], selectedFiles[index]];

                updateInput();
            });

            const remove = document.createElement("button");
            remove.type = "button";
            remove.className = "btn btn-sm btn-outline-danger";
            remove.textContent = "×";

            remove.addEventListener("click", function () {
                selectedFiles.splice(index, 1);
                updateInput();
            });

            actions.append(up, down, remove);
            item.append(name, actions);

            fileList.appendChild(item);
        });

        submitButton.disabled = selectedFiles.length === 0;
    }

    function addFiles(files) {

        const newFiles = Array.from(files);

        if (selectedFiles.length + newFiles.length > 20) {
            alert("Maximum 20 images are allowed.");
            return;
        }

        for (const file of newFiles) {

            if (!allowedTypes.includes(file.type)) {
                alert("Unsupported image format.");
                continue;
            }

            selectedFiles.push(file);
        }

        updateInput();
    }

    browseButton.addEventListener("click", function () {
        fileInput.click();
    });

    fileInput.addEventListener("change", function () {
        addFiles(fileInput.files);
    });

    dropArea.addEventListener("dragover", function (event) {
        event.preventDefault();
        dropArea.classList.add("dragover");
    });

    dropArea.addEventListener("dragleave", function () {
        dropArea.classList.remove("dragover");
    });

    dropArea.addEventListener("drop", function (event) {

        event.preventDefault();
        dropArea.classList.remove("dragover");

        addFiles(event.dataTransfer.files);
    });

    const uploadForms = document.querySelectorAll(
        'form[enctype="multipart/form-data"]'
    );

    uploadForms.forEach(form => {

        form.addEventListener("submit", function () {

            const button = form.querySelector(
                'button[type="submit"]'
            );

            if (button) {
                button.disabled = true;
                button.textContent = "Processing...";
            }

        });

    });

});
