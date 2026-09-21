let currentCustomerOrderId = null;
let currentTrackingOrderId = null;

function setCurrentCustomerOrderId(orderId) {
    currentCustomerOrderId = orderId;
}


function trackCustomerOrder() {
    if (currentCustomerOrderId === null) {
        console.error("No customer order selected.");
        return;
    }

    currentTrackingOrderId = currentCustomerOrderId;
    console.log("trackCustomerOrder function called ",currentTrackingOrderId);

    openTrackingModal(currentTrackingOrderId);
}



function openTrackingModal(orderId) {
    
    console.log("openTrackingModal function called",orderId);
    currentTrackingOrderId = orderId;

    const modal = document.getElementById("tracking-modal");

    modal.classList.remove("hidden");

    document.getElementById("tracking-order-number").textContent = `Order #FH${orderId}`;

    loadCustomerOrderTracking(orderId);
}



function closeTrackingModal() {
    document.getElementById("tracking-modal").classList.add("hidden");
}



async function loadCustomerOrderTracking(orderId) {

    try {

        const response = await apiFetch(`/api/customers/orders/${orderId}/tracking/`,
            {
                method: "GET",

            }
        );

        const data = await response.json();

        if (!response.ok) {

            throw new Error(
                data.detail || "Unable to load tracking information."
            );

        }

        console.log("Tracking data:", data);

        updateTrackingUI(data);

    } catch (error) {

        console.error(
            "Tracking error:",
            error
        );

        Swal.fire({
            icon: "error",
            title: "Tracking Unavailable",
            text: error.message
        });

    }
}






function updateTrackingUI(data) {

    const status = data.status;

    const statusElement =
        document.getElementById("tracking-status");

    const messageElement =
        document.getElementById("tracking-status-message");


    if (status === "ready") {

        statusElement.textContent =
            "Ready for Pickup";

        messageElement.textContent =
            "Your delivery partner is heading to the vendor.";

    }

    else if (status === "picked_up") {

        statusElement.textContent =
            "Order Picked Up";

        messageElement.textContent =
            "Your delivery partner has picked up your order.";

    }

    else if (status === "out_for_delivery") {

        statusElement.textContent =
            "Out for Delivery";

        messageElement.textContent =
            "Your order is on its way.";

    }

    else if (status === "delivered") {

        statusElement.textContent =
            "Delivered";

        messageElement.textContent =
            "Your order has been delivered.";

    }

    else {

        statusElement.textContent =
            status;

        messageElement.textContent =
            "Order status updated.";

    }


    // Delivery partner location

    if (
        data.delivery_partner &&
        data.delivery_partner.latitude &&
        data.delivery_partner.longitude
    ) {

        const latitude =
            parseFloat(data.delivery_partner.latitude);

        const longitude =
            parseFloat(data.delivery_partner.longitude);

        showDeliveryPartnerLocation(
            latitude,
            longitude
        );

    }

}




let trackingInterval = null;

function startOrderTracking(orderId) {

    stopOrderTracking();

    loadCustomerOrderTracking(orderId);

    trackingInterval = setInterval(
        function() {
            loadCustomerOrderTracking(orderId);
        },
        10000
    );

}


function stopOrderTracking() {

    if (trackingInterval) {

        clearInterval(trackingInterval);

        trackingInterval = null;
    }

}






function closeTrackingModal() {

    stopOrderTracking();

    if (deliveryMarker) {

        deliveryMarker.map = null;

        deliveryMarker = null;
    }

    trackingMap = null;

    document
        .getElementById("tracking-modal")
        .classList.add("hidden");
}





let trackingMap = null;
let deliveryMarker = null;
let googleMapReady = false;





async function initializeTrackingMap(latitude, longitude) {

    if (trackingMap) {
        return;
    }

    const { Map } = await google.maps.importLibrary("maps");

    trackingMap = new Map(
        document.getElementById("tracking-map"),
        {
            center: {
                lat: latitude,
                lng: longitude
            },

            zoom: 15,
            mapId: "DEMO_MAP_ID",
            streetViewControl: false,
            mapTypeControl: false,
            fullscreenControl: true
        }
    );

    googleMapReady = true;
}




async function initGoogleTrackingMap() {

    console.log("Google Maps loaded successfully.");

    googleMapReady = true;
}









async function showDeliveryPartnerLocation(latitude, longitude) {

    await initializeTrackingMap(latitude, longitude);

    const { AdvancedMarkerElement } =
        await google.maps.importLibrary("marker");

    const position = {
        lat: latitude,
        lng: longitude
    };

    if (!deliveryMarker) {

        const bikeElement = document.createElement("img");

        bikeElement.src = "/static/images/delivery-bike.png";

        bikeElement.style.width = "45px";
        bikeElement.style.height = "45px";
        bikeElement.style.objectFit = "contain";

        deliveryMarker = new AdvancedMarkerElement({
            map: trackingMap,
            position: position,
            content: bikeElement,
            title: "Delivery Partner"
        });

    } else {

        deliveryMarker.position = position;

    }

    trackingMap.setCenter(position);
}