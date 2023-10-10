function togglePassword() {
    var passwordInput = document.getElementById("pword");
    if (passwordInput.type === "password") {
        passwordInput.type = "text";
        event.target.textContent = 'Hide';
    }
    
    else {
        passwordInput.type = "password";
        event.target.textContent = "Show";
    }
}