function goToCustomer(latitude, longitude) {

    if (!latitude || !longitude) {

        Swal.fire({
            icon: "error",
            title: "Location Unavailable",
            text: "Customer location is not available."
        });

        return;
    }

    const googleMapsUrl =
        `https://www.google.com/maps/dir/?api=1&destination=${latitude},${longitude}`;

    window.open(googleMapsUrl, "_blank");
}