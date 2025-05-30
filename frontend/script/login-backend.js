// create account redirect
document.querySelector(".signup-container").addEventListener("click", () => {
  window.location.href = "./student/signup.html";
});

// form submission handler
document
  .getElementById("student-login-form")
  .addEventListener("submit", async function (event) {
    event.preventDefault(); // Prevent page reload on form submit

    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    try {
      const response = await fetch(
        "https://mess-registration-app-backend.onrender.com/login",
        {
          // Your Flask backend URL
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ email, password }), // Send as JSON
        }
      );

      const result = await response.json();

      console.log(result);

      // JWT
      if (response.ok) {
        const token = result.token;
        if (token) {
          // decoding to get email
          localStorage.clear();
          console.log("localStorage has been cleared.");
          const decoded = jwt_decode(token);
          localStorage.setItem("Current_User", decoded.email);
          localStorage.setItem(`jwtToken:${email}`, token);
          alert(result.message);
          window.location.href = "./student/dashboard.html";
        } else {
          alert("Login succeeded but no token received.");
        }
      } else {
        alert(result.error);
      }
    } catch (error) {
      alert(error);
    }
  });
