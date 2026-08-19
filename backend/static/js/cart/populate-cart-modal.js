
function populateCartModal(cartData) {

    const container = document.getElementById("cart-items-container");
    const cartCount = document.getElementById("cart-modal-count");
    const itemTotal = document.getElementById("cart-item-total");
    const deliveryFee = document.getElementById("cart-delivery-fee");
    const taxes = document.getElementById("cart-taxes"); 
    const grandTotal = document.getElementById("cart-grand-total");


    // ------------------------------------------------
    // Empty cart
    // ------------------------------------------------

    if (!cartData || !cartData.items || cartData.items.length === 0) {

        container.innerHTML = `
            <div class="text-center py-12">
                <i class="fa-solid fa-cart-shopping text-gray-300 text-5xl mb-5"></i>
                <h3 class="text-lg font-semibold text-gray-700">Your cart is empty</h3>
                <p class="text-sm text-gray-500 mt-2"> Add some delicious food to your cart.</p>
            </div>
        `;


        cartCount.innerText = "0 items";
        itemTotal.innerText = "₹0.00";
        deliveryFee.innerText = "₹0.00";
        taxes.innerText = "₹0.00";
        grandTotal.innerText = "₹0.00";

        return;
    }


    // ------------------------------------------------
    // Cart count
    // ------------------------------------------------

    const totalItems = cartData.total_items || 0;
    cartCount.innerText = `${totalItems} ${ totalItems === 1 ? "item" : "items"}`;


    // ------------------------------------------------
    // Generate cart items
    // ------------------------------------------------


    container.innerHTML = "";


    cartData.items.forEach(item => {

        const product = item.product;
        const imageUrl =
            product.image
                ? product.image
                : "https://via.placeholder.com/120?text=Food";


        const itemHTML = `
            <div class="flex gap-4 border-b pb-5">
                <!-- Product Image -->
                <img src="${imageUrl}" alt="${product.name}" class="w-20 h-20 object-cover rounded-2xl">

                <!-- Product Information -->
                <div class="flex-1">
                    <h3 class="font-semibold"> ${product.name}</h3>
                    <p class="text-sm text-gray-500"> ${product.vendor_name}</p>
                    <div class="flex items-center justify-between mt-3">

                        <!-- Quantity Controls -->
                        <div class="flex items-center gap-3">
                            <button onclick="decreaseCartItem(${item.id}, ${item.quantity})" class="w-8 h-8 rounded-full border border-gray-300 flex items-center justify-center text-lg hover:bg-gray-100">−</button>
                            <span class="font-medium"> ${item.quantity}</span>
                            <button  onclick="increaseCartItem(${item.id}, ${item.quantity})" class="w-8 h-8 rounded-full border border-gray-300 flex items-center justify-center text-lg hover:bg-gray-100">+</button>
                        </div>

                        <!-- Subtotal -->
                        <p class="font-semibold text-orange-600">₹${Number(item.subtotal).toFixed(2)}</p>
                    </div>


                    <!-- Remove -->
                    <button onclick="removeCartItem(${item.id})" class="text-xs text-red-500 hover:text-red-700 mt-3">Remove</button>

                </div>

            </div>

        `;


        container.insertAdjacentHTML("beforeend", itemHTML);

    });


    // ------------------------------------------------
    // Calculate totals
    // ------------------------------------------------

    const subtotal = Number(cartData.subtotal || 0);


    /*
        For now these are frontend values.

        Later, when you implement checkout,
        delivery fee and taxes should be calculated
        by the backend.
    */

  
const delivery =
    subtotal > 0 ? 40 : 0;

const tax =
    subtotal * 0.05;

const calculatedGrandTotal =
    subtotal +
    delivery +
    tax;


itemTotal.innerText =
    `₹${subtotal.toFixed(2)}`;

deliveryFee.innerText =
    `₹${delivery.toFixed(2)}`;

taxes.innerText =
    `₹${tax.toFixed(2)}`;

grandTotal.innerText =
    `₹${calculatedGrandTotal.toFixed(2)}`;
}