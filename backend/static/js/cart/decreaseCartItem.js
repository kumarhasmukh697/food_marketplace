async function decreaseCartItem( cartItemId, currentQuantity) {

    console.log( "Decrease cart item:", cartItemId, "Current quantity:", currentQuantity);

    // If quantity is already 1,
    // remove the item completely.
    if (currentQuantity <= 1) {
        await removeCartItem(cartItemId);
        return;
    }

    const newQuantity = currentQuantity - 1;

    await updateCartItemQuantity( cartItemId, newQuantity);
}