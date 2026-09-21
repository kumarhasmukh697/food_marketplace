async function updateDeliveryLocation(latitude, longitude) {

    try {
        const response = await apiFetch( "/api/delivery/profile/location/",
            {
                method: "PATCH",
                body: JSON.stringify({
                    current_latitude: latitude,
                    current_longitude: longitude,
                }),
            }
        );

        const data = await response.json();

        if (!response.ok) {
            throw new Error( data.detail || "Unable to update location." );
        }

        console.log("Delivery location updated:", data.current_latitude, data.current_longitude);

    } catch (error) {
        console.error("Failed to update delivery location:",error);
    }
}






function getDeliveryLocation() {
    if (!navigator.geolocation) {
        console.error("Geolocation is not supported by this browser.");
        return;
    }

    navigator.geolocation.getCurrentPosition(
        function (position) {

            const latitude = position.coords.latitude.toFixed(6);
            const longitude = position.coords.longitude.toFixed(6);
            console.log("Current location:", latitude, longitude);
            updateDeliveryLocation(latitude,longitude);
        },

        function (error) {
            console.error("Unable to get location:", error.message);
        },

        {
            enableHighAccuracy: true,
            timeout: 10000,
            maximumAge: 0
        }
    );
}






let deliveryLocationInterval = null;

function startDeliveryLocationTracking() {
    if (!navigator.geolocation) {
        console.error("Geolocation is not supported by this browser.");
        return;
    }

    // Get location immediately
    getDeliveryLocation();

    // Then update every 30 seconds
    deliveryLocationInterval = setInterval(getDeliveryLocation, 30000);
}





function stopDeliveryLocationTracking() {
    
    console.log("stop delivery location");
    if (deliveryLocationInterval) {
        clearInterval(deliveryLocationInterval);
        deliveryLocationInterval = null;
    }
}