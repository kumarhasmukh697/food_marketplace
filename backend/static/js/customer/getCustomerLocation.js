function getCustomerLocation() {

    if (!navigator.geolocation) {
        Swal.fire({
            icon: "error",
            title: "Location Not Supported",
            text: "Your browser does not support location services."
        });
        return;
    }


    navigator.geolocation.getCurrentPosition(

        async function(position) {

            const latitude = position.coords.latitude.toFixed(6);
            const longitude = position.coords.longitude.toFixed(6);

            console.log("Customer GPS:",latitude, longitude);


            const success = await updateCustomerLocation( latitude, longitude);


            if (success) {
                await Swal.fire({
                    icon: "success",
                    title: "Location Saved",
                    text: "Your location has been updated.",
                    timer: 1500,
                    showConfirmButton: false
                });
            }
        },


        function(error) {
            console.error( "Unable to get customer location:", error );
            Swal.fire({
                icon: "error",
                title: "Location Permission Required",
                text: error.message
            });
        },


        {
            enableHighAccuracy: true,
            timeout: 10000,
            maximumAge: 0
        }
    );
}







async function updateCustomerLocation(latitude, longitude) {

    const accessToken = localStorage.getItem("access");

    if (!accessToken) {
        console.error("Access token not found.");
        return false;
    }

    try {

        const response = await fetch( "/api/customers/profile/location/",
            {
                method: "PATCH",
                headers: {
                    "Authorization": `Bearer ${accessToken}`,
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                },
                body: JSON.stringify({
                    latitude: latitude,
                    longitude: longitude
                })
            }
        );

        const data = await response.json();

        if (!response.ok) {
            throw new Error(
                data.detail || "Unable to update vendor location."
            );
        }

        console.log("Customer location:", data.latitude, data.longitude);
        return true;

    } catch (error) {

        console.error( "Failed to update vendor location:", error);
        await Swal.fire({
            icon: "error",
            title: "Location Error",
            text: error.message
        });
        return false;
    }
}