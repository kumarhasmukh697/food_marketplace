async function openCartModal() {
    
    // Open modal
    document.getElementById("cart-modal").classList.remove("hidden");


    // Get container
    const cartItemsContainer = document.getElementById("cart-items-container");


    // Show loading
    cartItemsContainer.innerHTML = `
        <div class="text-center py-10 text-gray-500">
            <i class="fa-solid fa-spinner fa-spin text-2xl mb-3"></i>
            <p>Loading cart...</p>
        </div>
    `;


    try {

        const response = await apiFetch("/api/cart/",
            {
                method: "GET",
            }
        );


        const cartData = await response.json();

        // console.log("Cart Items:", cartData);


        if (!response.ok) {
            throw new Error(cartData.detail || `HTTP error! Status: ${response.status}`);
        }


        // Populate cart
        populateCartModal(cartData);


    } catch (error) {

        console.error("Failed to fetch cart:",error );


        cartItemsContainer.innerHTML = `
            <div class="text-center py-10">
                <i class="fa-solid fa-circle-exclamation text-red-500 text-3xl mb-3"></i>
                <p class="text-gray-500"> Unable to load your cart. </p>
            </div>
        `;
    }
}

