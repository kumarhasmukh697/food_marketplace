function getDeliveryProfile() {

    const accessToken = localStorage.getItem("access");

    if (!accessToken) {
        console.error("Access token not found.");
        return;
    }

    fetch("/api/delivery/profile/", {
        method: "GET",

        headers: {
            "Authorization": `Bearer ${accessToken}`,
            "Content-Type": "application/json"
        }
    })

    .then(response => {

        if (!response.ok) {
            throw new Error(
                `HTTP error! status: ${response.status}`
            );
        }

        return response.json();
    })

    .then(data => {

        console.log(
            "Fetched delivery profile data:",
            data
        );

        // ==========================================
        // User Information
        // ==========================================

        const firstName = document.querySelector(
            '#delivery-profile-form input[name="first_name"]'
        );

        const lastName = document.querySelector(
            '#delivery-profile-form input[name="last_name"]'
        );

        const phoneNumber = document.querySelector(
            '#delivery-profile-form input[name="phone_number"]'
        );


        if (firstName) {
            firstName.value = data.first_name || "";
        }

        if (lastName) {
            lastName.value = data.last_name || "";
        }

        if (phoneNumber) {
            phoneNumber.value = data.phone_number || "";
        }


        // ==========================================
        // Address
        // ==========================================

        const addressLine1 = document.querySelector(
            '#delivery-profile-form textarea[name="address_line_1"]'
        );

        const addressLine2 = document.querySelector(
            '#delivery-profile-form input[name="address_line_2"]'
        );

        const city = document.querySelector(
            '#delivery-profile-form input[name="city"]'
        );

        const state = document.querySelector(
            '#delivery-profile-form input[name="state"]'
        );

        const pincode = document.querySelector(
            '#delivery-profile-form input[name="pincode"]'
        );


        if (addressLine1) {
            addressLine1.value =
                data.address_line_1 || "";
        }

        if (addressLine2) {
            addressLine2.value =
                data.address_line_2 || "";
        }

        if (city) {
            city.value =
                data.city || "";
        }

        if (state) {
            state.value =
                data.state || "";
        }

        if (pincode) {
            pincode.value =
                data.pincode || "";
        }


        // ==========================================
        // Delivery Partner Information
        // ==========================================

        const vehicleType = document.querySelector(
            '#delivery-profile-form [name="vehicle_type"]'
        );

        const vehicleNumber = document.querySelector(
            '#delivery-profile-form input[name="vehicle_number"]'
        );

        const licenseNumber = document.querySelector(
            '#delivery-profile-form input[name="driving_license_number"]'
        );


        if (vehicleType) {
            vehicleType.value =
                data.vehicle_type || "";
        }

        if (vehicleNumber) {
            vehicleNumber.value =
                data.vehicle_number || "";
        }

        if (licenseNumber) {
            licenseNumber.value =
                data.driving_license_number || "";
        }


        // ==========================================
        // Profile Picture
        // ==========================================

        const profilePreview = document.getElementById(
            "profile-preview"
        );

        if (
            profilePreview &&
            data.profile_picture
        ) {

            profilePreview.src =
                data.profile_picture;
        }

    })

    .catch(error => {

        console.error(
            "Error fetching delivery profile:",
            error
        );

    });
}