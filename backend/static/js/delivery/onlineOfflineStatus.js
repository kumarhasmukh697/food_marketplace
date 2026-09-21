async function toggleDeliveryOnlineStatus() {
  
    const toggle = document.getElementById("delivery-online-toggle");
    const isCurrentlyOnline = toggle.classList.contains("bg-emerald-500");
    const newStatus = !isCurrentlyOnline;

  
    const data = await updateOnlineStatus(newStatus);

    if (!data) {
        return;
    }

    const statusText = document.getElementById("delivery-status-text");
    const circle =  document.getElementById("delivery-toggle-circle");


    // -----------------------------------------
    // Update UI
    // -----------------------------------------

    if (data.is_online) {
        toggle.classList.remove("bg-gray-300");
        toggle.classList.add("bg-emerald-500");
        circle.classList.remove("left-1");
        circle.classList.add("left-9");
        statusText.textContent = "You are online and available for deliveries.";

    } else {
        toggle.classList.remove("bg-emerald-500");
        toggle.classList.add("bg-gray-300");
        circle.classList.remove("left-9");
        circle.classList.add("left-1");
        statusText.textContent = "You are currently offline.";
    }
}





async function updateOnlineStatus(isOnline) {

    try {
        const response = await apiFetch("/api/delivery/profile/status/",
            {
                method: "PATCH",
                body: JSON.stringify({
                    is_online: isOnline
                })
            }
        );


        const data = await response.json();
        if (!response.ok) {

            throw new Error(
                data.detail || "Unable to update status."
            );
        }


        console.log("Delivery status:", data);


        // -----------------------------------------
        // Location tracking
        // -----------------------------------------

        if (data.is_online) {
            startDeliveryLocationTracking();

        } else {
            stopDeliveryLocationTracking();

        }

        return data;


    } catch (error) {

        console.error( "Failed to update online status:", error);
        await Swal.fire({
            icon: "error",
            title: "Unable to Update Status",
            text: error.message,
        });
        return null;
    }
}