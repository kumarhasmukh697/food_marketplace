async function updateVendorOrderStatus(orderId, newStatus) {

    try {

        const response = await apiFetch(`/api/orders/vendor/orders/${orderId}/status/`,
            {
                method: "PATCH",
                body: JSON.stringify({
                    status: newStatus
                }),
            }
        );


        const data = await response.json();
        console.log("Status response:", data);

        if (!response.ok) {
            throw new Error( data.detail || "Unable to update order status.");
        }


        // -----------------------------------------
        // Success
        // -----------------------------------------

        await Swal.fire({

            icon: "success",
            title: "Order Updated",
            text: `Order status changed to ${formatVendorOrderStatus(newStatus)}.`,
            timer: 2500,
            showConfirmButton: false,

        });


        // -----------------------------------------
        // If delivery partner was assigned
        // -----------------------------------------

        if (data.delivery_partner) {
            console.log("Delivery partner assigned:", data.delivery_partner);
        }

    }
    catch (error) {

        console.error("Failed to update order status:", error );
        await Swal.fire({
            icon: "error",
            title: "Update Failed",
            text: error.message,
        });


        // -----------------------------------------
        // Reload page so dropdown returns
        // to actual database value
        // -----------------------------------------

        window.location.reload();
    }
}






function formatVendorOrderStatus(status) {

    const statusMap = {

        confirmed: "Confirmed",
        preparing: "Preparing",
        ready: "Ready",
        picked_up: "Picked Up",
        out_for_delivery: "Out for Delivery",
        delivered: "Delivered",
        cancelled: "Cancelled",

    };

    return (
        statusMap[status] || status
    );
}