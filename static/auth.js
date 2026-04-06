document.addEventListener("DOMContentLoaded", function () {


    const passwordInput = document.getElementById("password");
    const strengthBar = document.getElementById("strength-bar");
    const strengthText = document.getElementById("strength-text");

    if (!passwordInput) {
        console.warn("Password input not found!");
    } else {
        passwordInput.addEventListener("input", () => {
            const password = passwordInput.value;


            
            let strength = 0;

           
            if (/[A-Z]/.test(password)) strength++;
            if (/[a-z]/.test(password)) strength++;
            if (/[0-9]/.test(password)) strength++;
            if (/[^A-Za-z0-9]/.test(password)) strength++;

            
            

            const strengthMap = [
                { width: "25%", color: "#dc3545", text: "Weak" },
                { width: "50%", color: "#ffc107", text: "Medium" },
                { width: "75%", color: "#0d6efd", text: "Good" },
                { width: "100%", color: "#198754", text: "Strong" },
            ];

            

            const level = Math.min(strength, 4) - 1;
            let { width, color, text } = strengthMap[level] || strengthMap[0];

            const submitBtn = document.getElementsByClassName("save-password")

            if (password.length < 6){
                strength = 0;
                width="0%"
                color="transparent"
                text= "password must be at least 6 characters";

                
            }

            strengthBar.style.width = width;
            strengthBar.style.background = color;
            strengthText.textContent = text;
        });
    }
});