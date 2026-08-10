document
    .getElementById("delivery-profile-form")
    .addEventListener("submit", saveDeliveryProfile);

async function saveDeliveryProfile() {

   

    const form = document.getElementById("delivery-profile-form");

    const formData = new FormData(form);

    try {

        const response = await fetch("/api/delivery/profile/", {

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