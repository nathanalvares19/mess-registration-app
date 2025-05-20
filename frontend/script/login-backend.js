document
  .getElementById("student-login-form")
  .addEventListener("submit", async function (event) {
    event.preventDefault(); // Prevent page reload on form submit

    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    try {
      const response = await fetch("http://localhost:5000/login", {
        // Your Flask backend URL
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }), // Send as JSON
      });

      const result = await response.json();

      if (response.ok) {
        alert(result.message); // Successful login
        window.location.href = "../student/dashboard.html"; // Redirect to dashboard (change if needed)
      } else {
        alert(result.message); // Show error message
      }
    } catch (error) {
      alert("Error connecting to backend");
      console.error(error);
    }
  });
