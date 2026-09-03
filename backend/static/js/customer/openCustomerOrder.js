async function openCustomerOrder(orderId) {
  
    const modal = document.getElementById("order-modal");
    modal.classList.remove("hidden");

    const accessToken = localStorage.getItem("access")

    try{
        const response = await fetch(`/api/orders/customer/view/${orderId}/`,{

                method: "GET",
                headers: {
                    "Authorization": `Bearer ${accessToken}`,
                    "Accept": "application/json",
                },
            }
        );

        const data = await response.json();
       
        
         if (!response.ok) {
            throw new Error( data.detail || "Unable to fetch order details.");

        }

        displayVendorOrder(data);
    }

    catch(error){

        console.error("Failed to load customer order:", error);
        modal.classList.add("hidden");
        await Swal.fire({
            icon: "error",
            title: "Unable to Load Order",
            text: error.message,

        });

    }
}





function displayVendorOrder(order) {

    // -----------------------------------------
    // Order information
    // -----------------------------------------

    document.getElementById("vendor-order-number").textContent =`Order #FH-${order.id}`;
    document.getElementById("vendor-order-status").textContent = formatVendorOrderStatus( order.status);
    document.getElementById("vendor-order-date").textContent = `Placed on ${formatVendorOrderDate( order.created_at)}`;
    document.getElementById( "vendor-order-total").textContent =`₹${order.total_amount}`;


    // -----------------------------------------
    // Customer
    // -----------------------------------------

    document.getElementById( "vendor-customer-name").textContent = order.customer_name;
    document.getElementById("vendor-customer-phone").textContent = order.customer_phone || "Not available";


    // -----------------------------------------
    // Address
    // -----------------------------------------

    


    let addressText = "Not available";

    if (order.delivery_address) {

        const address = order.delivery_address;

        addressText =
            `${address.address_line_1}, ` +
            `${address.address_line_2 ? address.address_line_2 + ", " : ""}` +
            `${address.city}, ` +
            `${address.state} - ` +
            `${address.pincode}`;
    }


    document.getElementById("vendor-customer-address").textContent = addressText;


    // -----------------------------------------
    // Bill
    // -----------------------------------------

    document.getElementById( "vendor-order-subtotal").textContent =`₹${order.subtotal}`;
    document.getElementById( "vendor-order-delivery-fee").textContent =`₹${order.delivery_fee}`;
    document.getElementById("vendor-order-tax").textContent =`₹${order.tax}`;
    // document.getElementById("vendor-order-discount").textContent =`₹${order.discount}`;
    document.getElementById("vendor-order-grand-total").textContent = `₹${order.total_amount}`;


    // -----------------------------------------
    // Order Items
    // -----------------------------------------

    displayVendorOrderItems( order.items);
}





function displayVendorOrderItems(items) {

    const container = document.getElementById("vendor-order-items");
    const template = document.getElementById("vendor-order-item-template");


    // Remove previous order's items
    container.replaceChildren();


    // Add every item
    items.forEach(item => {
        const itemElement =template.content.cloneNode(true);
        const image = itemElement.querySelector(".item-image");
        const name = itemElement.querySelector(".item-name");
        const quantity = itemElement.querySelector(".item-quantity");
        const subtotal = itemElement.querySelector(".item-subtotal");
       
    
        // Product image
        if (item.product_image) {
            image.src = item.product_image;
        }
        else {
            image.src = "/static/images/default-product.png";
        }


        // Product name
        name.textContent = item.product_name;
        // Quantity
        quantity.textContent = `Qty: ${item.quantity}`;
        // Subtotal
        subtotal.textContent = `₹${item.subtotal}`;
        // Add item to modal
        container.appendChild(itemElement);

    });
}



function formatVendorOrderStatus(status) {

    const statusMap = {

        pending_payment:
            "Payment Pending",

        confirmed:
            "Confirmed",

        preparing:
            "Preparing",

        ready:
            "Ready",

        out_for_delivery:
            "Out for Delivery",

        delivered:
            "Delivered",

        cancelled:
            "Cancelled",

    };


    return (
        statusMap[status] ||
        status
    );
}




function formatVendorOrderDate(dateString) {

    const date =
        new Date(dateString);


    return date.toLocaleString(
        "en-IN",
        {
            day: "2-digit",
            month: "short",
            year: "numeric",
            hour: "2-digit",
            minute: "2-digit",
        }
    );
}



function closeOrderModal() {
    document.getElementById('order-modal').classList.add('hidden');
}