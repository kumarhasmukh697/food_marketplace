async function increaseCartItem(cartItemId, currentQuantity) {

    console.log( "Increase cart item:", cartItemId, "Current quantity:", currentQuantity);
    const newQuantity = currentQuantity + 1;

    await updateCartItemQuantity( cartItemId, newQuantity);
}