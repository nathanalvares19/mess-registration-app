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
    console.log("Logged in user email:", data.email);
    email = data.email;
    document.querySelector(".email").textContent = email;
  })
  .catch((error) => {
    console.error(error);
  });

// unregister

const unregisterDiv = document.querySelector(".unregister-button");

function unregisterHandler() {
  fetch("http://localhost:5000/unregister-user", {
    method: "GET",
    credentials: "include",
  })
    .then((response) => {
      if (!response.ok) throw new Error("Not logged in");
      return response.json();
    })
    .then((data) => {
      document.querySelector(".status").textContent = `Not registered`;
      alert(data.message);

      // Visually disable and remove click handler
      disableUnregisterButton();
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

// document.querySelector(".unregister-button").addEventListener("click", () => {
//   fetch("http://localhost:5000/unregister-user", {
//     method: "GET",
//     credentials: "include", // important to send cookies/session info
//   })
//     .then((response) => {
//       if (!response.ok) throw new Error("Not logged in");
//       return response.json();
//     })
//     .then((data) => {
//       document.querySelector(".status").textContent = `Not registered`;
//       alert(data.message);
//     })
//     .catch((error) => {
//       console.error(error);
//     });
// });

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

  // document.getElementById(
  //   "current-date"
  // ).textContent = `${day}${suffix} ${month} ${year}`;

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
    const response = await fetch("http://localhost:5000/mess_data", {
      credentials: "include",
    });

    if (!response.ok) {
      const errorData = await response.json();
      console.log(errorData.error);
      throw new Error(errorData.error || "Failed to fetch mess data");
    }

    const result = await response.json();

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
    // alert("Error: " + error.message);
    console.log("Error: " + error.message);
  }
});

// logout handler
document.querySelector(".logout").addEventListener("click", () => {
  alert("User successfully logged out");
  window.location.href = "./login.html";
});
