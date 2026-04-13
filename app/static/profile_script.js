document.addEventListener('DOMContentLoaded', () => {
    checkAuthentication();
  });

  function getCookie(name) {
    const cookies = document.cookie.split('; ');
    const token = cookies.find(cookie => cookie.startsWith(name + '='));
    if (!token) {
      window.location.href = 'login.html'; // if not signed in, redirect to login page
    }
    const extracted_name = token.split('=');
    return extracted_name[1];
}

