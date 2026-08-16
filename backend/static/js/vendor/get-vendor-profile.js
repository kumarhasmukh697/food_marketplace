function getvendorProfile() {
    const accessToken = localStorage.getItem("access");
 
    if (!accessToken) {
        console.error("Access token not found.");
        return;
    }

    fetch("/api/vendors/profile/", {
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
        // console.log("Fetched vendor profile data:", data);
      
        // =========================
        // Restaurant Information
        // =========================

        const shopName = document.querySelector(
            'input[name="shop_name"]'
        );

        const restaurantAddress = document.querySelector(
            'textarea[name="address_line_1"]'
        );

        if (shopName) {
            shopName.value = data.shop_name || "";
        }

        if (restaurantAddress) {
            restaurantAddress.value = data.address_line_1 || "";
        }

        // =========================
        // Owner Information
        // =========================

        const firstName = document.querySelector(
            'input[name="first_name"]'
        );

        const lastName = document.querySelector(
            'input[name="last_name"]'
        );

        const phoneNumber = document.querySelector(
            'input[name="phone_number"]'
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


        // =========================
        // Address Information
        // =========================

        const city = document.querySelector(
            'input[name="city"]'
        );

        const state = document.querySelector(
            'input[name="state"]'
        );

        const pincode = document.querySelector(
            'input[name="pincode"]'
        );

        if (city) {
            city.value = data.city || "";
        }

        if (state) {
            state.value = data.state || "";
        }

        if (pincode) {
            pincode.value = data.pincode || "";
        }


        // =========================
        // Opening / Closing Time
        // =========================

        const openingTime = document.querySelector(
            'input[name="opening_time"]'
        );

        const closingTime = document.querySelector(
            'input[name="closing_time"]'
        );

        if (openingTime) {
            openingTime.value = formatTime(data.opening_time);
        }

        if (closingTime) {
            closingTime.value = formatTime(data.closing_time);
        }


        // =========================
        // Profile Picture
        // =========================

        const profilePreview = document.getElementById(
            "profile-preview"
        );

        if (profilePreview && data.profile_picture) {
            profilePreview.src = data.profile_picture;
        }
    })
    .catch(error => {
        console.error("Error fetching vendor profile:", error);
    });
    }


    // Convert Django time like "11:00:00" to
    // HTML input[type="time"] format "11:00"
    function formatTime(time) {
    if (!time) {
        return "";
    }

    return time.substring(0, 5);
}