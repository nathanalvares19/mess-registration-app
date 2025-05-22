window.addEventListener("DOMContentLoaded", async () => {
  try {
    const response = await fetch("http://localhost:5000/get-history", {
      credentials: "include",
    });
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
  window.location.href = "./dashboard.html";
});
