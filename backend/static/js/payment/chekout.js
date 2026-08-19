function openCheckoutModal() {
    console.log("hello ");
    document.getElementById('cart-modal').classList.add('hidden');   // close cart
    document.getElementById('checkout-modal').classList.remove('hidden'); // open payment
}

function closeCheckoutModal() {
    document.getElementById('checkout-modal').classList.add('hidden');
}