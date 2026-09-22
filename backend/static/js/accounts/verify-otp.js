 document.getElementById('otp-form').addEventListener('submit', async function (e) {
    e.preventDefault();
    
    const email = sessionStorage.getItem("verify_email");
    const otp = document.getElementById('otp').value;

    const response = await fetch('/api/accounts/verify-otp/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, otp })
    });

    const data = await response.json();

    if (response.ok) {
        
        await Swal.fire({
                title: "Verify Email",
                text: data.message || "Email verified successfully!",
                icon: "success",
                confirmButtonText: "OK",
            });
        sessionStorage.removeItem("verify_email");
        window.location.href = '/login/';
    } else {
        alert(data.detail || JSON.stringify(data));
    }
});
