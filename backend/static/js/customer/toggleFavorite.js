async function toggleFavorite(vendorId) {
    
    const accessToken = localStorage.getItem("access");

    try{
        const response = await fetch(`/api/wishlist/favorites/${vendorId}/`,{
           
            method:'POST',
            headers: {
                "Authorization": `Bearer ${accessToken}`,
                "Accept": "application/json",
                },
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