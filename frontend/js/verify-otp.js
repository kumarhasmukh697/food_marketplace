 
document.getElementById('otp-form').addEventListener('submit', async function (e) {
    e.preventDefault();

    const email = document.getElementById('email').value;
    const otp = document.getElementById('otp').value;

    const response = await fetch('http://127.0.0.1:8000/api/accounts/verify-otp/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, otp })
    });

    const data = await response.json();

    if (response.ok) {
        alert('Account verified successfully!');
        window.location.href = 'login.html';
    } else {
        alert(data.detail || JSON.stringify(data));
    }
});
