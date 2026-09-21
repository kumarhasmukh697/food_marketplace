async function logout() {

    const refreshToken = localStorage.getItem("refresh");

    if (!refreshToken) {
        localStorage.removeItem("access");
        localStorage.removeItem("refresh");
        localStorage.removeItem("user");

        window.location.href = "/login/";
        return;
    }

    try {

        const response = await apiFetch(
            "/api/accounts/logout/",
            {
                method: "POST",
                body: JSON.stringify({
                    refresh: refreshToken,
                }),
            }
        );

        const data = await response.json();

        if (response.ok) {

            localStorage.removeItem("access");
            localStorage.removeItem("refresh");
            localStorage.removeItem("user");

            await Swal.fire({
                title: "Logged Out",
                text: data.message || "You have been logged out successfully.",
                icon: "success",
                confirmButtonText: "OK",
            });

            window.location.href = "/login/";

        } else {

            // Even if server rejects logout, clear local authentication
            localStorage.removeItem("access");
            localStorage.removeItem("refresh");
            localStorage.removeItem("user");

            await Swal.fire({
                title: "Logged Out",
                text: "You have been logged out.",
                icon: "success",
                confirmButtonText: "OK",
            });

            window.location.href = "/login/";
        }

    } catch (error) {
        console.error("Logout error:", error);
        // Clear local authentication anyway
        localStorage.removeItem("access");
        localStorage.removeItem("refresh");
        localStorage.removeItem("user");
        window.location.href = "/login/";
    }
}