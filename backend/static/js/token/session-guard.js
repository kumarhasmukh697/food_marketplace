(function redirectExpiredSession() {
    const refreshToken = localStorage.getItem("refresh");

    function clearSessionAndRedirect() {
        localStorage.removeItem("access");
        localStorage.removeItem("refresh");
        localStorage.removeItem("user");
        window.location.replace("/");
    }

    if (!refreshToken) {
        clearSessionAndRedirect();
        return;
    }

    try {
        const payload = refreshToken.split(".")[1];
        const decodedPayload = JSON.parse(
            decodeURIComponent(
                atob(payload.replace(/-/g, "+").replace(/_/g, "/"))
                    .split("")
                    .map(character => `%${(`00${character.charCodeAt(0).toString(16)}`).slice(-2)}`)
                    .join("")
            )
        );

        if (!decodedPayload.exp || decodedPayload.exp <= Math.floor(Date.now() / 1000)) {
            clearSessionAndRedirect();
        }
    } catch (error) {
        clearSessionAndRedirect();
    }
})();