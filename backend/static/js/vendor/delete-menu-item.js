

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