const token = localStorage.getItem("jwtToken");

window.addEventListener("DOMContentLoaded", async () => {
  try {
    const response = await fetch(
      "https://mess-registration-app-backend.onrender.com/get-history",
      {
        Authorization: `Bearer ${token}`,
      }
    );
    const data = await response.json();

    const tbody = document.querySelector("#history-table tbody");
    data.forEach((entry, index) => {
      const row = document.createElement("tr");

      row.innerHTML = `
        <td>${entry.status}</td>
        <td>${entry.timestamp}</td>
        <td>${entry.mess}</td>
        <td>${entry.plan}</td>
      `;

      tbody.appendChild(row);
    });
  } catch (err) {
    console.error("Failed to load history:", err);
  }
});

// back button
document.querySelector(".back-button").addEventListener("click", () => {
  window.location.href = "/student/dashboard.html";
});
