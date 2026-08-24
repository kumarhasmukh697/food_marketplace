async function openCheckoutModal() {

    console.log("Starting checkout...");
    const accessToken = localStorage.getItem("access");

    if (!accessToken) {

        await Swal.fire({
            icon: "error",
            title: "Authentication Required",
            text: "Please login before proceeding to checkout.",
        });

        return;
    }

    try {

        // ==================================================
        // STEP 1
        // Create our Django Order
        // ==================================================

        const checkoutResponse = await fetch("/api/orders/checkout/",
            {
                method: "POST",
                headers: {
                    "Authorization": `Bearer ${accessToken}`,
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({}),
            }
        );

        const checkoutData = await checkoutResponse.json();

        console.log("Checkout response:", checkoutData);

        if (!checkoutResponse.ok) {
            throw new Error(
                checkoutData.detail ||
                "Unable to create checkout."
            );
        }

        const orderId = checkoutData.order.id;

        console.log("Django Order ID:", orderId);


        // ==================================================
        // STEP 2
        // Create Razorpay Order
        // ==================================================

        const razorpayResponse = await fetch("/api/payments/create-order/",
            {
                method: "POST",
                headers: {
                    "Authorization": `Bearer ${accessToken}`,
                    "Content-Type": "application/json",
                },

                body: JSON.stringify({
                    order_id: orderId,
                }),
            }
        );

        const razorpayData = await razorpayResponse.json();

        console.log( "Razorpay order response:", razorpayData);

        if (!razorpayResponse.ok) {
            throw new Error(
                razorpayData.detail ||
                "Unable to create Razorpay order."
            );
        }


        // ==================================================
        // STEP 3
        // Open Razorpay Checkout
        // ==================================================

        openRazorpayCheckout(razorpayData);

    }
    catch (error) {

        console.error("Checkout failed:", error);
        await Swal.fire({
            icon: "error",
            title: "Checkout Failed",
            text: error.message ||
                "Something went wrong.",

        });
    }
}




function openRazorpayCheckout(razorpayData) {

    console.log("Opening Razorpay Checkout...");

    const options = {

        // ------------------------------------------
        // Razorpay Key ID
        // ------------------------------------------

        key: razorpayData.key_id,


        // ------------------------------------------
        // Amount in paise
        // ------------------------------------------

        amount: razorpayData.amount_in_paise,


        // ------------------------------------------
        // Currency
        // ------------------------------------------

        currency: razorpayData.currency,


        // ------------------------------------------
        // Razorpay Order ID
        // ------------------------------------------

        order_id: razorpayData.razorpay_order_id,


        // ------------------------------------------
        // Display information
        // ------------------------------------------

        name: "FoodHub",

        description: "FoodHub Order Payment",


        // ------------------------------------------
        // Prefill customer information
        // ------------------------------------------

        prefill: {

            name: localStorage.getItem( "username" ) || "",

            email: localStorage.getItem( "email") || "",

        },


        // ------------------------------------------
        // Theme
        // ------------------------------------------

        theme: {

            color: "#f97316",

        },


        // ------------------------------------------
        // Payment success handler
        // ------------------------------------------

        handler: function ( response) {
            console.log( "Razorpay payment successful:", response);
            handlePaymentSuccess(response, razorpayData.order_id);
        },


        // ------------------------------------------
        // Modal closed
        // ------------------------------------------

        modal: {
            ondismiss: function () {
                console.log("Razorpay Checkout closed.");

            },

        },

    };


    const razorpay = new Razorpay(options);


    razorpay.on("payment.failed", function (response) {

            console.error("Payment failed:", response);
            Swal.fire({
                icon: "error",
                title: "Payment Failed",
                text: response.error.description || "Payment failed.",

            });

        }
    );


    razorpay.open();
}




async function handlePaymentSuccess(response, orderId) {

    console.log( "Payment successful. Starting verification..." );
    console.log( "Razorpay response:", response);
    const accessToken = localStorage.getItem("access");

    try {

        const verifyResponse = await fetch( "/api/payments/verify/",
            {
                method: "POST",
                headers: {
                    "Authorization": `Bearer ${accessToken}`,
                    "Content-Type": "application/json",
                },

                body: JSON.stringify({

                    razorpay_order_id: response.razorpay_order_id,
                    razorpay_payment_id: response.razorpay_payment_id,
                    razorpay_signature: response.razorpay_signature,

                }),
            }
        );

        const verifyData = await verifyResponse.json();
        console.log( "Payment verification response:", verifyData);

        if (!verifyResponse.ok) {
            throw new Error( verifyData.detail || "Payment verification failed." );
        }

        await Swal.fire({

            icon: "success",
            title: "Payment Successful",
            text: "Your order has been confirmed.",

        });

        // -----------------------------------------
        // Close cart modal
        // -----------------------------------------

        if ( typeof closeCartModal === "function") {
            closeCartModal();
        }

        // -----------------------------------------
        // Later we can redirect to order details
        // -----------------------------------------

        console.log( "Confirmed Order ID:", verifyData.order_id);

    }
    catch (error) {

        console.error( "Payment verification error:", error);
        await Swal.fire({
            icon: "error",
            title: "Payment Verification Failed",
            text: error.message || "Unable to verify payment.",

        });

    }
}