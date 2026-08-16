async function saveEditedItem() {

    // ==========================================
    // Get Product ID
    // ==========================================

    const productId =
        document.getElementById("edit-index").value;


    if (!productId) {

        alert("Product ID not found.");

        return;
    }


    // ==========================================
    // Get Form Values
    // ==========================================

    const name =
        document.getElementById("edit-name").value.trim();

    const price =
        document.getElementById("edit-price").value;

    const category =
        document.getElementById("edit-dish-category").value;

    const description =
        document.getElementById("edit-desc").value.trim();

    const stock =
        document.getElementById("edit-stock").value;

    const isAvailable =
        document.getElementById("edit-available").checked;

    const isVeg =
        document.getElementById("edit-dish-veg").checked;

    const image =
        document.getElementById(
            "edit-profile-picture"
        ).files[0];


    // ==========================================
    // Validation
    // ==========================================

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


    // ==========================================
    // FormData
    // ==========================================

    const formData = new FormData();

    formData.append(
        "name",
        name
    );

    formData.append(
        "price",
        price
    );

    formData.append(
        "category",
        category
    );

    formData.append(
        "description",
        description
    );

    formData.append(
        "stock",
        stock
    );

    formData.append(
        "is_available",
        isAvailable
    );

    formData.append(
        "is_veg",
        isVeg
    );


    // ==========================================
    // Image
    // ==========================================

    if (image) {

        formData.append(
            "image",
            image
        );

    }


    // ==========================================
    // PATCH Request
    // ==========================================

    try {

        const response = await fetch(
            `${API.products}${productId}/`,
            {

                method: "PATCH",

                headers: {
                    "Authorization":
                        `Bearer ${getAccessToken()}`
                },

                body: formData

            }
        );


        const data =
            await response.json();


        console.log(
            "Updated product:",
            data
        );


        // ==========================================
        // Error
        // ==========================================

        if (!response.ok) {

            console.error(data);

            alert(
                data.detail ||
                "Failed to update product."
            );

            return;
        }


        // ==========================================
        // Find Existing Card
        // ==========================================

        const existingCard =
            document.getElementById(
                `product-${productId}`
            );


        // ==========================================
        // Replace Existing Card
        // ==========================================

        if (existingCard) {

            existingCard.outerHTML =
                createProductCard(data);

        }


        // ==========================================
        // Success
        // ==========================================

        alert(
            "Product updated successfully."
        );


        // ==========================================
        // Close Modal
        // ==========================================

        closeEditModal();

    }
    catch (error) {

        console.error(error);

        alert(
            "Something went wrong."
        );

    }

}