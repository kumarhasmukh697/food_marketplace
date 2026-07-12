async function logout() {

    // getting acces and refresh token from local storage
    const accessToken = localStorage.getItem("access");
    const refreshToken = localStorage.getItem("refresh");
    
    // if not found access or refresh token in local storage it means means user is already logged out redirect to login page
    if (!accessToken || !refreshToken) {
        window.location.href = "/login/";
        return;
    }

    try {
        const response = await fetch("http://127.0.0.1:8000/api/accounts/logout/", {
            
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${accessToken}`,
            },
            body: JSON.stringify({
                refresh: refreshToken,
            }),
        });
       
        const data = await response.json();
      
        if (response.ok) {
           
            // Remove JWT tokens
            localStorage.removeItem("access");
            localStorage.removeItem("refresh");
            localStorage.removeItem("user");

            await Swal.fire({
                title: "Logged Out",
                text: data.message,
                icon: "success",
                confirmButtonText: "OK",
            });
          
            window.location.href = "/login/";

        } else {

            await Swal.fire({
                title: "Logout Failed",
                text: data.detail || "Something went wrong.",
                icon: "error",
            });

        }

    } catch (error) {


        await Swal.fire({
            title: "Server Error",
            text: "Unable to connect to the server.",
            icon: "error",
        });

    }
}