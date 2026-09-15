async function updateDeliveryOrderStatus(orderId, newStatus) {

    const accessToken = localStorage.getItem("access");

    try {

        const response = await fetch(`/api/delivery/orders/${orderId}/status/`,
            {
                method: "PATCH",
                headers: {
                    "Authorization": `Bearer ${accessToken}`,
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                },
                body: JSON.stringify({
                   status: newStatus
                })
            }
        );


        const data = await response.json();


        if (!response.ok) {
            throw new Error(data.detail || "Unable to update order status.");
        }


        console.log("Delivery order status:", data);

        await Swal.fire({
            icon: "success",
            title: "Order Updated",
            text: `Order status changed to ${formatDeliveryStatus(newStatus)}.`,
            timer: 1500,
            showConfirmButton: false
        });


        // Refresh dashboard
        window.location.reload();


    } catch (error) {
        console.error("Failed to update delivery status:", error);
        await Swal.fire({
            icon: "error",
            title: "Update Failed",
            text: error.message
        });

    }
}





function formatDeliveryStatus(status) {

    const statusMap = {
        ready: "Ready for Pickup",
        picked_up: "Picked Up",
        out_for_delivery: "Out for Delivery",
        delivered: "Delivered",
    };

    return statusMap[status] || status;
}