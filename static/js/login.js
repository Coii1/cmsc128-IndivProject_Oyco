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
            body: JSON.stringify(data),
            credentials: "include"
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

// ang problem nmn di kay if damo2 tumok ka user ma sulit2 mn sya call
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
            body: JSON.stringify(data),
            credentials: "include"
        });

        const result = await response.json();
        document.getElementById("loginMessage").textContent = result.message;

        if (response.ok) {
            console.log("Login success:", result);
            console.log("username:", result.username);
            document.getElementById("username").textContent = result.username;
            showTodoApp();
        } else {
            console.error("Login failed:", result.message);
        }
    } catch (error) {
        //console.error('Error logging in:', error);
    }
});

window.addEventListener("DOMContentLoaded", async () => {
    try {
        const res = await fetch("http://127.0.0.1:5000/api/check_session", {
            credentials: "include"
        });

        if (res.ok) {
            const sessionData = await res.json();
            console.log(res)


            // If the session has a user_id, show todo app immediately
            if (sessionData.user_id) {
                showTodoApp();  
                console.log(sessionData.user_id)
                document.getElementById("username").textContent = sessionData.first_name;
                console.log("session exists")
            } else {
                document.getElementById("loginContainer").style.display = "block";
                console.log("login now")
            }
        } else {
            document.getElementById("loginContainer").style.display = "block";
        }
    } catch (error) {
        console.error("Error checking session", error);
        document.getElementById("loginContainer").style.display = "block";
    }
});


function showTodoApp() {
    console.log("showTodoApp function reached")
    document.getElementById("loginContainer").style.display = "none";
    document.getElementById("todoContainer").style.display = "flex";
    fetchTasks();  // load tasks after login
    //check_session()
    
}