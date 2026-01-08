const backendUrl = "http://127.0.0.1:8000";

async function loadTransactions() {
  try {
    const response = await fetch(`${backendUrl}/sms?category=transactions`);
    const data = await response.json();
    const container = document.getElementById("sms-container");
    container.innerHTML = "";

    data.forEach(sms => {
      const card = document.createElement("div");
      card.className = "p-4 border rounded-lg shadow bg-white dark:bg-background-dark mb-3";
      card.innerHTML = `
        <p class="font-semibold">${sms.text}</p>
        <p class="text-sm text-gray-600">Category: ${sms.category}</p>
        <p class="text-xs text-gray-400">${new Date(sms.timestamp).toLocaleString()}</p>
      `;
      container.appendChild(card);
    });
  } catch (err) {
    console.error("Error loading transactions:", err);
  }
}

document.addEventListener("DOMContentLoaded", loadTransactions);
