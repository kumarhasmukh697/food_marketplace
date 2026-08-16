
async function saveNewItem() {

    // Get all form values
    const name = document.getElementById("dish-name").value.trim();
    const price = document.getElementById("dish-price").value;
    const category = document.getElementById("dish-category").value;
    const description = document.getElementById("dish-desc").value.trim();
    const stock = document.getElementById("dish-stock").value;
    const isAvailable = document.getElementById("dish-available").checked;
    const image = document.getElementById("profile_picture").files[0];
    const isVeg = document.getElementById("dish-veg").checked;

    

    // Basic validation
    if (!name) {
        alert("Please enter product name.");
        return;
    }

    if (!price || Number(price) <= 0) {
        alert("Please enter a valid price.");
        return;
    }

    if (!category) {
        alert("Please select a category.");
        return;
    }

    if (!stock || Number(stock) < 0) {
        alert("Please enter valid stock.");
        return;
    }

    // Create FormData
    const formData = new FormData();

    formData.append("name", name);
    formData.append("price", price);
    formData.append("category", category);
    formData.append("description", description);
    formData.append("stock", stock);
    formData.append("is_available", isAvailable);
    formData.append("is_veg", isVeg);
    if (image) {
        formData.append("image", image);
    }


    try {

        const response = await fetch(API.products, {

            method: "POST",

            headers: {
                "Authorization": `Bearer ${getAccessToken()}`
            },

            body: formData

        });

        const data = await response.json();
        console.log(data);

        if (!response.ok) {
            console.error(data);
            alert("Failed to create product.");
            return;
        }

        console.log("Product Created:", data);
        alert("Product added successfully.");

        closeAddModal();

        // Clear form
        clearProductForm();

        const menuGrid = document.getElementById("menu-items-grid");
        if (menuGrid) {
            menuGrid.insertAdjacentHTML(
                "beforeend",
                createProductCard(data)
            );
        }

    }
    catch (error) {

        console.error(error);

        alert("Something went wrong.");

    }

}
