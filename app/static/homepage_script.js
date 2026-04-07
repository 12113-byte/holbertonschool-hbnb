//Check authentication and hides the login button if already logged in
document.addEventListener('DOMContentLoaded', () => {
    const cookies = document.cookie.split(';');
    const token = cookies.find(c => c.trim().statsWith('token='));
    const loginLink = document.querySelector('a[href="/login"]');
    if (token && loginLink) {
        loginLink.style.display = 'none;'
    }
});
