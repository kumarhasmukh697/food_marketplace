async function updateCartItemQuantity( cartItemId, newQuantity) {

    console.log("Updating cart item:", cartItemId, "New quantity:", newQuantity);

    try {

        const response = await fetch( `http://127.0.0.1:8000/api/cart/items/${cartItemId}/`,
            {
                method: "PATCH",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${localStorage.getItem("access")}`,
                },

                body: JSON.stringify({
                    quantity: newQuantity,
                }),
            }
        );

        const data = await response.json();

        console.log("Update quantity response:", data);

        if (!response.ok) {

            await Swal.fire({
                icon: "error",
                title: "Unable to update quantity",
                text:
                    data.detail ||
                    JSON.stringify(data),
            });

            return;
        }

        /*
         * Your CartItemUpdateView returns
         * the updated CartSerializer directly.
         */
        populateCartModal(data);

        // Update navbar cart count
        const cartCount = document.getElementById("cart-count");

        if (cartCount) {
            cartCount.innerText = data.total_items;
        }

    } catch (error) {

        console.error("Error updating cart quantity:", error);

        await Swal.fire({
            icon: "error",
            title: "Server Error",
            text: "Unable to update cart.",
        });
    }
}