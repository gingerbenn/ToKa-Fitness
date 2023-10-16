function togglePassword() {
    var passwordInput = document.getElementById("pword");
    if (passwordInput.type === "password") {
        passwordInput.type = "text";
    }
    
    else {
        passwordInput.type = "password";
    }
}