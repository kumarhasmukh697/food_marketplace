document.getElementById('sign-form').addEventListener('submit', async function (e) {
    e.preventDefault();
    
    // payload is the the data send with the request to the backend
    const payload = {
        username: document.getElementById('username').value,
        email: document.getElementById('email').value,
        password: document.getElementById('password').value,
        role: document.getElementById('role').value
    };
    
    sessionStorage.setItem("verify_email", payload.email);
   
    
    // Send a POST request to the backend API for user registration
    const response = await fetch('http://127.0.0.1:8000/api/accounts/register/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
    });

    // 
    const data = await response.json();
    console.log(data);
    

   if (response.ok) {
    await Swal.fire({
        title: "Good job!",
        text: "Registration successful! Please verify your OTP.",
        icon: "success"
    });

   window.location.replace("/verify-otp/");
   } else {

    let errorMessage = "";

    for (const key in data) {
        errorMessage += `${key}: ${data[key].join(", ")}\n`;
    }

    await Swal.fire({
        title: "Registration Failed",
        text: errorMessage,
        icon: "error"
    });
}
});
