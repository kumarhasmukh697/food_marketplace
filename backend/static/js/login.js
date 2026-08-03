document.getElementById("login-form").addEventListener("submit", async function (e) {
    e.preventDefault();

    // Data to send to the backend
    const payload = {
        email: document.getElementById("email").value,
        password: document.getElementById("password").value,
    };

    try {
        // Send login request
        const response = await fetch("http://127.0.0.1:8000/api/accounts/login/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(payload),
        });

        const data = await response.json();

        if (response.ok) {

            // Store JWT tokens
            localStorage.setItem("access", data.access);
            localStorage.setItem("refresh", data.refresh);

            // Store logged-in user information
            localStorage.setItem("user", JSON.stringify(data.user));

            await Swal.fire({
                title: "Login Successful!",
                text: `Welcome ${data.user.username}`,
                icon: "success",
                confirmButtonText: "Continue",
            });

            // Redirect based on user role
            const dashboardMap = {
                customer: "/home/",
                vendor: "/v-dashboard/",
                delivery: "/d-dashboard/"
            };

            window.location.href = dashboardMap[data.user.role];
            // window.location.replace(dashboardMap[data.user.role]);
           

        } else {
            await Swal.fire({
                title: "Login Failed",
                text: data.error || "Invalid email or password.",
                icon: "error",
            });
        }

    } catch (error) {
        console.error(error);

        await Swal.fire({
            title: "Server Error",
            text: "Unable to connect to the server. Please try again later.",
            icon: "error",
        });
    }
});


