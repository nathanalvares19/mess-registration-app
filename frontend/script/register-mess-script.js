document.addEventListener("DOMContentLoaded", function () {
  // Set current date with format like "5th May 2025"
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
  const suffixes = ["th", "st", "nd", "rd"];
  const relevantDigits = day % 100;
  const suffix =
    suffixes[(relevantDigits - 20) % 10] ||
    suffixes[relevantDigits] ||
    suffixes[0];

  document.getElementById(
    "current-date"
  ).textContent = `${day}${suffix} ${month} ${year}`;

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
  document.getElementById("active-week").textContent = activeWeek;

  // Calculate and display active month
  const displayMonth = currentDate.toLocaleString("default", { month: "long" });
  document.getElementById(
    "active-month"
  ).textContent = `${displayMonth} ${year}`;

  // Handle form submission
  document
    .getElementById("registration-form")
    .addEventListener("submit", function (e) {
      e.preventDefault();

      // Get form values
      const messType = document.querySelector(
        'input[name="mess-type"]:checked'
      ).value;
      const planType = document.querySelector(
        'input[name="plan-type"]:checked'
      ).value;

      // Store in session storage for use in dashboard
      sessionStorage.setItem("messType", messType);
      sessionStorage.setItem("planType", planType);

      // Redirect to dashboard
      window.location.href = "dashboard.html";
    });
});
