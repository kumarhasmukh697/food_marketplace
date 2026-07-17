const API = {
    products: "http://127.0.0.1:8000/api/products/",
    categories: "http://127.0.0.1:8000/api/categories/"
};


function closeAddModal() {
    document.getElementById('add-item-modal').classList.add('hidden');
}



function getAccessToken() {
    return localStorage.getItem("access");
}

async function fetchCategories(selectId) {

    try {

        const response = await fetch(API.categories, {

            method: "GET",

            headers: {
                Authorization: `Bearer ${getAccessToken()}`,
                "Content-Type": "application/json"
            }

        });

        if (!response.ok) {
            throw new Error("Unable to load categories.");
        }

        const categories = await response.json();

        const categorySelect = document.getElementById(selectId);

        categorySelect.innerHTML =
            '<option value="">Select Category</option>';

        categories.forEach(category => {

            const option = document.createElement("option");

            option.value = category.id;

            option.textContent = category.name;

            categorySelect.appendChild(option);

        });

    }
    catch (error) {

        console.error(error);

    }

}


function clearProductForm() {

    // Clear form
    document.getElementById("dish-name").value = "";
    document.getElementById("dish-price").value = "";
    document.getElementById("dish-category").value = "";
    document.getElementById("dish-desc").value = "";
    document.getElementById("dish-stock").value = "";
    document.getElementById("dish-available").checked = true;
    document.getElementById("dish-image").value = "";
}



async function addNewItem() {
    document.getElementById('add-item-modal').classList.remove('hidden'); 
    // Call the function
    await fetchCategories("dish-category");

}



async function saveNewItem() {

    // Get all form values
    const name = document.getElementById("dish-name").value.trim();
    const price = document.getElementById("dish-price").value;
    const category = document.getElementById("dish-category").value;
    const description = document.getElementById("dish-desc").value.trim();
    const stock = document.getElementById("dish-stock").value;
    const isAvailable = document.getElementById("dish-available").checked;
    const image = document.getElementById("dish-image").files[0];

    

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

        
        await loadProducts();

    }
    catch (error) {

        console.error(error);

        alert("Something went wrong.");

    }

}



async function loadProducts() {

    const menuGrid = document.getElementById("menu-items-grid");

    // Clear previous cards
    menuGrid.innerHTML = "";

    try {

        const response = await fetch(API.products, {

            method: "GET",

            headers: {
                "Authorization": `Bearer ${getAccessToken()}`,
                "Content-Type": "application/json"
            }

        });

        if (!response.ok) {
            throw new Error("Failed to fetch products.");
        }

        const products = await response.json();
        // console.log(products);

        products.forEach(product => {

        menuGrid.insertAdjacentHTML(
            "beforeend",
            createProductCard(product)
        );

});
    }
    catch (error) {

        console.error("Error loading products:", error);

    }

}

document.addEventListener("DOMContentLoaded", function () {
    loadProducts();
});



function createProductCard(product) {
    
    const imageUrl = product.image
        ? product.image
        : "https://via.placeholder.com/600x400?text=No+Image";

    const availabilityBadge = product.is_available
        ? `
        <span class="px-4 py-1 bg-green-100 text-green-700 text-xs font-medium rounded-full">
            Available
        </span>
        `
        : `
        <span class="px-4 py-1 bg-red-100 text-red-700 text-xs font-medium rounded-full">
            Unavailable
        </span>
        `;

    const stockStatus = product.stock > 0
        ? `
        <div class="flex items-center gap-1.5">
            <div class="w-2 h-2 bg-emerald-500 rounded-full"></div>
            <span class="text-emerald-600 text-xs font-medium">
                In Stock
            </span>
        </div>
        `
        : `
        <div class="flex items-center gap-1.5">
            <div class="w-2 h-2 bg-red-500 rounded-full"></div>
            <span class="text-red-600 text-xs font-medium">
                Out of Stock
            </span>
        </div>
        `;

    return `
        <div  id="product-${product.id}" class="bg-white rounded-3xl overflow-hidden shadow-sm card-hover">
            <img src="${imageUrl}" class="w-full h-52 object-cover" alt="${product.name}">
            <div class="p-6">
                <div class="flex justify-between items-start">
                    <div>
                        <h3 class="font-semibold text-xl"> ${product.name}</h3>
                        <p class="text-emerald-600 font-medium mt-1">₹${product.price}</p>
                    </div>
                    ${availabilityBadge}
                </div>
                <p class="text-gray-500 text-sm mt-3 line-clamp-2"> ${product.description || ""}</p>
                <div class="mt-4 flex items-center justify-between text-sm">
                    <div class="flex items-center gap-2">
                        <span class="text-gray-500">Stock:</span>
                        <span class="font-medium text-emerald-600"> ${product.stock} units</span>
                    </div>
                    ${stockStatus}
                </div>
                <div class="flex gap-3 mt-6">
                    <button onclick="editMenuItem(${product.id})" class="flex-1 border border-gray-300 hover:bg-gray-50 py-3 rounded-2xl text-sm font-medium flex items-center justify-center gap-2">
                        <i class="fa-solid fa-pen"></i>
                        Edit
                    </button>

                    <button onclick="deleteMenuItem(${product.id})" class="flex-1 border border-red-200 hover:bg-red-50 text-red-600 py-3 rounded-2xl text-sm font-medium flex items-center justify-center gap-2">
                        <i class="fa-solid fa-trash"></i>
                        Delete
                    </button>
                </div>
            </div>
        </div>
    `;
}



async function deleteMenuItem(productId) {

    const result = await Swal.fire({
        title: "Delete Product?",
        text: "This action cannot be undone.",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#dc2626",
        cancelButtonColor: "#6b7280",
        confirmButtonText: "Delete",
        cancelButtonText: "Cancel"
    });

    if (!result.isConfirmed) {
        return;
    }

    try {

        const response = await fetch(`${API.products}${productId}/`, {

            method: "DELETE",

            headers: {
                Authorization: `Bearer ${getAccessToken()}`
            }

        });

        if (!response.ok) {
            throw new Error("Failed to delete product.");
        }

        // Remove the card from the page
        const productCard = document.getElementById(`product-${productId}`);

        if (productCard) {
            productCard.remove();
        }

        Swal.fire({
            icon: "success",
            title: "Deleted!",
            text: "Product deleted successfully.",
            timer: 1500,
            showConfirmButton: false
        });

    }
    catch (error) {

        console.error(error);

        Swal.fire({
            icon: "error",
            title: "Error",
            text: "Unable to delete product."
        });

    }

}




async function editMenuItem(productId) {

    try {

        const response = await fetch(`${API.products}${productId}/`, {

            method: "GET",

            headers: {
                Authorization: `Bearer ${getAccessToken()}`,
                "Content-Type": "application/json"
            }

        });

        if (!response.ok) {
            throw new Error("Unable to fetch product.");
        }

        const product = await response.json();

        // Populate category dropdown
        await fetchCategories("edit-category");

        // Store id
        document.getElementById("edit-index").value = product.id;

        // Fill inputs
        document.getElementById("edit-name").value = product.name;

        document.getElementById("edit-price").value = product.price;

        document.getElementById("edit-desc").value =
            product.description || "";

        document.getElementById("edit-stock").value =
            product.stock;

        document.getElementById("edit-available").checked =
            product.is_available;
       

        // If using nested serializer
        document.getElementById("edit-category").value =
            product.category.id;

        // If serializer returns integer instead
        // document.getElementById("edit-category").value = product.category;

        // Open modal
        document
            .getElementById("edit-item-modal")
            .classList.remove("hidden");

    }
    catch (error) {

        console.error(error);

        Swal.fire({
            icon: "error",
            title: "Error",
            text: "Unable to load product."
        });

    }

}


async function saveEditedItem() {

    const productId =
        document.getElementById("edit-index").value;

    const formData = new FormData();

    formData.append(
        "name",
        document.getElementById("edit-name").value.trim()
    );

    formData.append(
        "price",
        document.getElementById("edit-price").value
    );

    formData.append(
        "category",
        document.getElementById("edit-category").value
    );

    formData.append(
        "description",
        document.getElementById("edit-desc").value.trim()
    );

    formData.append(
        "stock",
        document.getElementById("edit-stock").value
    );

    formData.append(
        "is_available",
        document.getElementById("edit-available").checked
       
    );

    try {

        const response = await fetch(
            `${API.products}${productId}/`,
            {
                method: "PATCH",

                headers: {
                    Authorization: `Bearer ${getAccessToken()}`
                },

                body: formData
            }
        );

        if (!response.ok) {
            throw new Error("Failed to update product.");
        }

        Swal.fire({
            icon: "success",
            title: "Updated!",
            text: "Product updated successfully.",
            timer: 1500,
            showConfirmButton: false
        });

        closeEditModal();

        await loadProducts();

    }
    catch (error) {

        console.error(error);

        Swal.fire({
            icon: "error",
            title: "Error",
            text: "Unable to update product."
        });

    }

}

function closeEditModal() {
    document.getElementById('edit-item-modal').classList.add('hidden');
}


