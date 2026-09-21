async function apiFetch(url, options = {}) {
    let accessToken = localStorage.getItem("access");
    const isFormData = options.body instanceof FormData;

    options.headers = {
        ...(options.headers || {}),
        "Authorization": `Bearer ${accessToken}`,
        "Accept": "application/json",
    };

    if (!isFormData) {
        options.headers["Content-Type"] = "application/json";
    }

    let response = await fetch(url, options);

    // Access token expired
    if (response.status === 401) {

        const refreshed = await refreshAccessToken();

        if (!refreshed) {
            // Refresh token also expired/invalid
            localStorage.removeItem("access");
            localStorage.removeItem("refresh");
            localStorage.removeItem("user");

            window.location.href = "/login/";
            return;
        }

        // Get newly generated access token
        accessToken = localStorage.getItem("access");

        // Update Authorization header
        options.headers["Authorization"] = `Bearer ${accessToken}`;

        // Retry original request
        response = await fetch(url, options);
    }

    return response;
}







async function refreshAccessToken() {

    const refreshToken = localStorage.getItem("refresh");

    if (!refreshToken) {
        return false;
    }

    try {

        const response = await fetch("/api/accounts/token/refresh/",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                },
                body: JSON.stringify({
                    refresh: refreshToken
                })
            }
        );

        if (!response.ok) {
            return false;
        }

        const data = await response.json();

        localStorage.setItem("access", data.access);

        return true;

    } catch (error) {
        console.error("Token refresh failed:", error);
        return false;
    }
}