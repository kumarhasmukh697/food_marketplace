
function clearProductForm() {

    // Clear form
    document.getElementById("dish-name").value = "";
    document.getElementById("dish-price").value = "";
    document.getElementById("dish-category").value = "";
    document.getElementById("dish-desc").value = "";
    document.getElementById("dish-stock").value = "";
    document.getElementById("dish-available").checked = true;

    const fileInput = document.getElementById("profile_picture");
    if (fileInput) {
        fileInput.value = "";
    }

    const preview = document.getElementById("profile-preview");
    if (preview) {
        preview.src = "";
        preview.alt = "";
    }

    const previewName = document.getElementById("profile-picture-name");
    if (previewName) {
        previewName.textContent = "PNG, JPG, supported";
    }
}
