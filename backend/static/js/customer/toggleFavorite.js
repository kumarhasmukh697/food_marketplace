async function toggleFavorite(vendorId) {

    try{
        const response = await apiFetch(`/api/wishlist/favorites/${vendorId}/`,{
            method:'POST',
        })

        const data = await response.json();
        console.log( "favorite:", data);

        if (!response.ok) {
            throw new Error( data.detail || "Unable to fetch order details.");

        }

    }
    catch(error){
        console.error("Failed to toggle favorite:", error);
        await Swal.fire({
            icon: "error",
            title: "Unable to add to Favorites",
            text: error.message,

        });
    }
}