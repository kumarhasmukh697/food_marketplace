
document.getElementById("customer-profile-form").addEventListener("submit", saveCustomerProfile);

async function saveCustomerProfile() { 
    console.log("hello");
   
    // getting the form element from Customer profile modal
    const form = document.getElementById("customer-profile-form");
   
    // creating a FormData object to hold the form data, including the file input
    const formData = new FormData(form);

    try {

        const response = await fetch("/api/customers/profile/", {

            method: "PATCH",

            headers: {
                Authorization: `Bearer ${localStorage.getItem("access")}`,
            },

            body: formData,

        });

        const data = await response.json();

        if (response.ok) {

            await Swal.fire({

                icon: "success",

                title: "Success",

                text: "Profile updated successfully.",

            });

            closeProfileModal();

        } else {

            await Swal.fire({

                icon: "error",

                title: "Update Failed",

                text: data.detail || JSON.stringify(data),

            });

        }

    } catch (error) {

        console.error(error);

        await Swal.fire({

            icon: "error",

            title: "Server Error",

            text: "Unable to connect to the server.",

        });

    }

}