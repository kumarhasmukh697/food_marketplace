// add product to cart
async function addToCart(productId) {
    const cart_count = document.getElementById('cart-count');
    try{
        const response = await fetch("http://127.0.0.1:8000/api/cart/add/",

        {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${localStorage.getItem("access")}`,
            },
            body: JSON.stringify({
                product_id: productId,
                quantity: 1,

      })
        }
        );

        const data = await response.json();
        console.log("Cart response:", data);

        if (!response.ok) {

            console.error("Failed to add product:",data);

            await Swal.fire({
                icon: "error",
                title: "Unable to add product",
                text: data.detail || JSON.stringify(data),
            });

            return;
        }

        // Update cart count ONLY after successful API request
        const cartCount = document.getElementById("cart-count");

        if (cartCount) {
            cartCount.innerText =
                Number(cartCount.innerText) + 1;
        }
    }
    catch(error){
        console.error("Failed to add item to cart",error);
        await Swal.fire({
            icon: "error",
            title: "Server Error",
            text: "Unable to connect to the server.",
        });
    }
}
