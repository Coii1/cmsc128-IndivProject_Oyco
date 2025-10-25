// Function to display the sign-up form when the button is clicked
function openForm() {
    document.getElementById("signUp").style.display = "block";  // Show the signup form
    document.getElementById("signIn").style.display = "none";  // Hide the sign-in form
}

// Switch to the sign-up form when the 'Sign Up' button is clicked from the Sign-In form
document.getElementById("signUpButton").addEventListener("click", function() {
    document.getElementById("signUp").style.display = "block";  // Show the signup form
    document.getElementById("signIn").style.display = "none";  // Hide the sign-in form
});

// Switch to the sign-in form when the 'Sign In' button is clicked from the Sign-Up form
document.getElementById("signInButton").addEventListener("click", function() {
    document.getElementById("signIn").style.display = "block";  // Show the sign-in form
    document.getElementById("signUp").style.display = "none";  // Hide the signup form
});

document.getElementById("signUpForm").addEventListener("submit", async (e) => {
    e.preventDefault();
    try {
        // Grab form data
        const form = e.target;
        const data = {
            firstName: form.fname.value,
            lastName: form.lname.value,
            email: form.email.value,
            password: form.password.value
        };

        // Send the data to Flask backend as JSON
        const response = await fetch("/accounts", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data)
        });



        const result = await response.json();
        document.getElementById("signUpMessage").textContent = result.message;
        // Clear form fields
        document.getElementById("signUpForm").reset();
        
    } catch (error) {
        console.error('Error creating account:', error);
        //error message if existing na ang email
    }
});

document.getElementById("signInForm").addEventListener("submit", async (e) => {
    e.preventDefault();

    const form = e.target;
    const data = {
        email: form.email.value,
        password: form.password.value
    };

    try {
        const response = await fetch("/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data)
        });

        const result = await response.json();
        document.getElementById("loginMessage").textContent = result.message;

        if (response.ok) {
            console.log("Login success:", result);
            window.location.href = "/logged";
        } else {
            console.error("Login failed:", result.message);
        }
    } catch (error) {
        //console.error('Error logging in:', error);
    }
});