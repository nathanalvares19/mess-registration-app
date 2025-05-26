const registerButton = document.getElementById("go-to-mess-registration");
const email = localStorage.getItem(`Current_User`);
const token = localStorage.getItem(`jwtToken:${email}`);

// get email of user
fetch("https://mess-registration-app-backend.onrender.com/current-user", {
  method: "GET",
  headers: {
    Authorization: `Bearer ${token}`,
  },
})
  .then((response) => {
    if (!response.ok) throw new Error("Not logged in");
    return response.json();
  })
  .then((data) => {
    console.log("Logged in user email:", data.email);
    document.querySelector(".email").textContent = data.email;

    const isRegistered = localStorage.getItem(`isRegistered:${email}`);

    if (isRegistered === "true") {
      disableRegisterButton();
      enableUnregisterButton();
    } else {
      enableRegisterButton();
      disableUnregisterButton();
    }
  })
  .catch((error) => {
    console.error(error.message);
  });

// Register click handler
function registerHandler() {
  window.location.href = "register-mess.html";

  disableRegisterButton();
  enableUnregisterButton();
}

// Function to disable the register button
function disableRegisterButton() {
  registerButton.removeEventListener("click", registerHandler);
  registerButton.classList.add("disabled");
  registerButton.style.pointerEvents = "none";
  registerButton.style.opacity = "0.5";
}

// Function to enable the register button
function enableRegisterButton() {
  registerButton.addEventListener("click", registerHandler);
  registerButton.classList.remove("disabled");
  registerButton.style.pointerEvents = "auto";
  registerButton.style.opacity = "1";
}

// Attach the register click handler initially
registerButton.addEventListener("click", registerHandler);

// status update
const status = document.querySelector(".status");

// unregister
const unregisterDiv = document.querySelector(".unregister-button");

function unregisterHandler() {
  fetch("https://mess-registration-app-backend.onrender.com/unregister-user", {
    method: "GET",
    headers: {
      Authorization: `Bearer ${token}`,
    },
  })
    .then((response) => {
      const data = response.json();
      if (!response.ok) throw new Error(data.error);
      return data;
    })
    .then((data) => {
      document.querySelector(".status").textContent = `Not registered`;
      alert(data.message);

      disableUnregisterButton(); // Disable unregister
      enableRegisterButton(); // Enable register
      console.log("User unregistered");

      // set registration state
      localStorage.setItem(`isRegistered:${email}`, "false");
    })
    .catch((error) => {
      console.error(error);
    });
}

// Attach the handler
unregisterDiv.addEventListener("click", unregisterHandler);

// Function to disable the div
function disableUnregisterButton() {
  unregisterDiv.removeEventListener("click", unregisterHandler);
  unregisterDiv.classList.add("disabled");
  unregisterDiv.style.pointerEvents = "none";
  unregisterDiv.style.opacity = "0.5";
  // unregisterDiv.textContent = "Unregistered"; // Optional: update text
}

// Function to re-enable the div (call this after user registers)
function enableUnregisterButton() {
  unregisterDiv.addEventListener("click", unregisterHandler);
  unregisterDiv.classList.remove("disabled");
  unregisterDiv.style.pointerEvents = "auto";
  unregisterDiv.style.opacity = "1";
  unregisterDiv.textContent = "Unregister"; // Optional: restore original text
}

document.addEventListener("DOMContentLoaded", async function () {
  // active week/month
  // Set current date with format like "20th May 2025"
  const currentDate = new Date();
  const day = currentDate.getDate();
  const monthNames = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
  ];
  const month = monthNames[currentDate.getMonth()];
  const year = currentDate.getFullYear();

  // Add ordinal suffix to day
  function getOrdinalSuffix(day) {
    if (day > 3 && day < 21) return "th";
    switch (day % 10) {
      case 1:
        return "st";
      case 2:
        return "nd";
      case 3:
        return "rd";
      default:
        return "th";
    }
  }

  const suffix = getOrdinalSuffix(day);

  // Calculate and display active week
  const startDate = new Date(currentDate);
  startDate.setDate(startDate.getDate() - startDate.getDay()); // Start of week (Sunday)
  const endDate = new Date(startDate);
  endDate.setDate(endDate.getDate() + 6); // End of week (Saturday)

  // Format dates for week display
  const formatDate = (date) => {
    const d = date.getDate();
    const m = date.toLocaleString("default", { month: "short" });
    return `${d} ${m}`;
  };

  const activeWeek = `${formatDate(startDate)} - ${formatDate(endDate)}`;

  // Calculate and display active month
  const displayMonth = currentDate.toLocaleString("default", { month: "long" });

  // fetch mess data
  try {
    const response = await fetch(
      "https://mess-registration-app-backend.onrender.com/mess_data",
      {
        method: "GET",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    );

    if (!response.ok) {
      document.querySelector(".status").textContent = "Not registered";
      const errorData = await response.json();
      throw new Error(errorData);
    }

    const result = await response.json();
    localStorage.setItem(`isRegistered:${email}`, "true");

    let activePeriod = "";

    if (result.plan === "Weekly") {
      activePeriod = activeWeek;
    } else if (result.plan === "Monthly") {
      activePeriod = displayMonth;
    }

    document.querySelector(
      ".status"
    ).textContent = `Registered for ${result.mess}: ${result.plan} (${activePeriod})`;
    enableUnregisterButton();
  } catch (error) {
    console.log(error.error);
  }
});

// logout handler
document.querySelector(".logout").addEventListener("click", () => {
  alert("User successfully logged out");
  localStorage.removeItem(`jwtToken:${email}`);
  localStorage.removeItem(`Current_User`);
  localStorage.removeItem(`isRegistered:${email}`);
  window.location.href = "/index.html";
});

// history button
document.querySelector(".history-container").addEventListener("click", () => {
  window.location.href = "/student/history.html";
});
