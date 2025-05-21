// registration redirect
document
  .getElementById("go-to-mess-registration")
  .addEventListener("click", () => {
    window.location.href = "register-mess.html"; // Adjust if needed
  });

// status update
const status = document.querySelector(".status");
email = "";

// get email of user
fetch("http://localhost:5000/current-user", {
  method: "GET",
  credentials: "include", // important to send cookies/session info
})
  .then((response) => {
    if (!response.ok) throw new Error("Not logged in");
    return response.json();
  })
  .then((data) => {
    // console.log("Logged in user email:", data.email);
    email = data.email;
  })
  .catch((error) => {
    console.error(error);
  });

// fetch mess data
fetch("http://localhost:5000/mess_data")
  .then((response) => {
    if (!response.ok) {
      throw new Error("Failed to fetch JSON: " + response.status);
    }
    return response.json(); // Parse JSON from response
  })
  .then((data) => {
    console.log(data); // Your JSON data as a JS object/array
  })
  .catch((error) => {
    console.error("Error:", error);
  });

document.addEventListener("DOMContentLoaded", async function () {
  try {
    const response = await fetch("http://localhost:5000/mess_data", {
      method: "GET",
      credentials: "include",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ mess: messType, plan: planType }),
    });

    const result = await response.json();

    if (response.ok) {
      alert(result.message);
      // sessionStorage.setItem("messType", messType);
      // sessionStorage.setItem("planType", planType);
      window.location.href = "dashboard.html";
    } else {
      alert("Error: " + result.message);
    }
  } catch (error) {
    alert("Network error: " + error.message);
  }
});
