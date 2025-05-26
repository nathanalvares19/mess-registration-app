const email = localStorage.getItem(`Current_User`);
const token = localStorage.getItem(`jwtToken:${email}`);

window.addEventListener("DOMContentLoaded", async () => {
  try {
    const response = await fetch(
      "https://mess-registration-app-backend.onrender.com/get-history",
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    );

    if (!response.ok) {
      window.location.href = "/index.html";
      throw new Error("Not logged in");
    }

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
    console.error(err);
  }
});

// back button
document.querySelector(".back-button").addEventListener("click", () => {
  window.location.href = "/student/dashboard.html";
});
