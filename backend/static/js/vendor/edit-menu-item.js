function previewProfilePicture(event) {
        const file = event.target.files[0];

        if (!file) return;

        document.getElementById("profile-preview").src =
            URL.createObjectURL(file);

        document.getElementById("profile-picture-name").textContent =
            file.name;
    }






async function editMenuItem(productId) {

    try {

        // ==========================================
        // Fetch Product
        // ==========================================

        const response = await fetch(
            `${API.products}${productId}/`,
            {
                method: "GET",

                headers: {
                    Authorization:
                        `Bearer ${getAccessToken()}`,

                    "Content-Type":
                        "application/json"
                }
            }
        );


        if (!response.ok) {

            throw new Error(
                "Unable to fetch product."
            );

        }


        const product =
            await response.json();


        console.log(
            "Fetched product:",
            product
        );


        // ==========================================
        // Fetch categories for EDIT modal
        // ==========================================

        await fetchCategories(
            "edit-dish-category"
        );


        // ==========================================
        // Product ID
        // ==========================================

        document.getElementById(
            "edit-index"
        ).value = product.id;


        // ==========================================
        // Product Name
        // ==========================================

        document.getElementById(
            "edit-name"
        ).value = product.name || "";


        // ==========================================
        // Price
        // ==========================================

        document.getElementById(
            "edit-price"
        ).value = product.price || "";


        // ==========================================
        // Description
        // ==========================================

        document.getElementById(
            "edit-desc"
        ).value =
            product.description || "";


        // ==========================================
        // Stock
        // ==========================================

        document.getElementById(
            "edit-stock"
        ).value =
            product.stock ?? "";


        // ==========================================
        // Availability
        // ==========================================

        document.getElementById(
            "edit-available"
        ).checked =
            Boolean(product.is_available);


        // ==========================================
        // Vegetarian
        // ==========================================

        document.getElementById(
            "edit-dish-veg"
        ).checked =
            Boolean(product.is_veg);


        // ==========================================
        // Category
        // ==========================================

        const categorySelect =
            document.getElementById(
                "edit-dish-category"
            );


        let categoryId = null;


        if (
            product.category !== undefined
        ) {

            if (
                product.category !== null &&
                typeof product.category === "object"
            ) {

                categoryId =
                    product.category.id;

            }
            else {

                categoryId =
                    product.category;

            }

        }
        else if (
            product.category_id !== undefined
        ) {

            categoryId =
                product.category_id;

        }


        if (
            categoryId !== null &&
            categoryId !== undefined
        ) {

            categorySelect.value =
                String(categoryId);

        }


        // ==========================================
        // Existing Product Image
        // ==========================================

        const imagePreview =
            document.getElementById(
                "edit-profile-preview"
            );

        const imageName =
            document.getElementById(
                "edit-profile-picture-name"
            );


        if (product.image) {

            imagePreview.src =
                product.image;

            imageName.textContent =
                "Current image";

        }
        else {

            imagePreview.src = "";

            imageName.textContent =
                "PNG, JPG, supported";

        }


        // ==========================================
        // Open Modal
        // ==========================================

        document
            .getElementById("edit-item-modal")
            .classList.remove("hidden");

    }

    catch (error) {

        console.error(
            "Error loading product:",
            error
        );

        Swal.fire({
            icon: "error",
            title: "Error",
            text: "Unable to load product."
        });

    }
}