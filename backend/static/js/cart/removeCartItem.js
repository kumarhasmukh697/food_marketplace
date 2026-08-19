async function removeCartItem(cartItemId) {

    console.log("Remove cart item:", cartItemId);

    try {

        const response = await fetch(`http://127.0.0.1:8000/api/cart/items/${cartItemId}/remove/`,
            {
                method: "DELETE",
                headers: {
                    "Authorization": `Bearer ${localStorage.getItem("access")}`,
                },
            }
        );

        const data = await response.json();

        console.log("Remove response:", data);

        if (!response.ok) {

            await Swal.fire({
                icon: "error",
                title: "Unable to remove item",
                text: data.detail || JSON.stringify(data),
            });

            return;
        }

        // Cart became completely empty
        if (!data.cart) {

            populateCartModal({
                items: [],
                total_items: 0,
                subtotal: 0,
            });

            // Update navbar cart count
            const cartCount = document.getElementById("cart-count");

            if (cartCount) {
                cartCount.innerText = "0";
            }

            return;
        }

        // Update modal with latest cart
        populateCartModal(data.cart);

        // Update navbar count
        const cartCount = document.getElementById("cart-count");

        if (cartCount) {
            cartCount.innerText = data.cart.total_items;
        }

    } catch (error) {

        console.error( "Error removing cart item:", error);

        await Swal.fire({
            icon: "error",
            title: "Server Error",
            text: "Unable to remove item from cart.",
        });
    }
}