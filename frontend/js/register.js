document.getElementById('sign-form').addEventListener('submit', async function (e) {
    e.preventDefault();

    const payload = {
        username: document.getElementById('username').value,
        email: document.getElementById('email').value,
        password: document.getElementById('password').value,
        role: document.getElementById('role').value
    };
    console.log(payload.username);

    const response = await fetch('http://127.0.0.1:8000/api/accounts/register/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
    });

    const data = await response.json();

    if (response.ok) {
        alert('Registration successful! Please verify your OTP.');
        window.location.href = 'verify-otp.html';
    } else {
        alert(data.detail || JSON.stringify(data));
    }
});
