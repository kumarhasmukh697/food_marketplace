function getCustomerProfile() {

    const accessToken = localStorage.getItem("access");

    if (!accessToken) {
        console.error("Access token not found.");
        return;
    }

    fetch("/api/customers/profile/", {
        method: "GET",

        headers: {
            "Authorization": `Bearer ${accessToken}`,
            "Content-Type": "application/json"
        }
    })
    .then(response => {

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        return response.json();
    })
    .then(data => {

        console.log("Fetched customer profile data:", data);


        // ==========================================
        // Personal Information
        // ==========================================

        const firstName = document.querySelector(
            '#customer-profile-form input[name="first_name"]'
        );

        const lastName = document.querySelector(
            '#customer-profile-form input[name="last_name"]'
        );

        const phoneNumber = document.querySelector(
            '#customer-profile-form input[name="phone_number"]'
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
        // Address Information
        // ==========================================

        const addressLine1 = document.querySelector(
            '#customer-profile-form textarea[name="address_line_1"]'
        );

        const city = document.querySelector(
            '#customer-profile-form input[name="city"]'
        );

        const state = document.querySelector(
            '#customer-profile-form input[name="state"]'
        );

        const pincode = document.querySelector(
            '#customer-profile-form input[name="pincode"]'
        );


        if (addressLine1) {
            addressLine1.value = data.address_line_1 || "";
        }

        if (city) {
            city.value = data.city || "";
        }

        if (state) {
            state.value = data.state || "";
        }

        if (pincode) {
            pincode.value = data.pincode || "";
        }


        // ==========================================
        // Preferences
        // ==========================================

        const dietaryPreference = document.querySelector(
            '#customer-profile-form select[name="dietary_preference"]'
        );

        const spiceLevel = document.querySelector(
            '#customer-profile-form select[name="spice_level"]'
        );


        if (dietaryPreference) {
            dietaryPreference.value =
                data.dietary_preference || "";
        }

        if (spiceLevel) {
            spiceLevel.value =
                data.spice_level || "";
        }


        // ==========================================
        // Profile Picture
        // ==========================================

        const profilePreview = document.getElementById(
            "profile-preview"
        );

        if (profilePreview && data.profile_picture) {
            profilePreview.src = data.profile_picture;
        }

    })
    .catch(error => {

        console.error(
            "Error fetching customer profile:",
            error
        );

    });
}