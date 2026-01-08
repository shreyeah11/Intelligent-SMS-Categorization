// sms.js
const backendUrl = "http://127.0.0.1:8000"; // update if your FastAPI runs on a different URL

async function loadMessages(category) {
    try {
        const response = await fetch(`${backendUrl}/sms?category=${category}`);
        const data = await response.json();
        const container = document.getElementById("sms-container");
        container.innerHTML = "";

        if (data.length === 0) {
            container.innerHTML = `<p class="text-center text-gray-500 dark:text-gray-400">No messages in this category</p>`;
            return;
        }

        data.forEach(sms => {
            const card = document.createElement("div");
            card.className = "group flex cursor-pointer items-center gap-4 px-4 py-3 hover:bg-primary/5 dark:hover:bg-primary/10";
            card.innerHTML = `
                <img alt="${category}" class="h-12 w-12 rounded-full object-cover" src="https://via.placeholder.com/48?text=${category[0].toUpperCase()}">
                <div class="flex-1">
                    <p class="font-semibold text-slate-800 dark:text-slate-200">${sms.text}</p>
                    <p class="text-sm text-slate-600 dark:text-slate-400">Category: ${sms.category}</p>
                    <p class="text-xs text-gray-400">${new Date(sms.timestamp).toLocaleString()}</p>
                </div>
                <button class="hidden rounded-full bg-primary/10 px-3 py-1 text-sm font-semibold text-primary group-hover:block dark:bg-primary/20">Unsubscribe</button>
            `;
            container.appendChild(card);
        });
    } catch (err) {
        console.error("Error fetching messages:", err);
    }
}

// Auto-load messages on DOMContentLoaded if a container has data-category
document.addEventListener("DOMContentLoaded", () => {
    const container = document.getElementById("sms-container");
    if (!container) return;

    const category = container.getAttribute("data-category");
    if (!category) {
        console.error("Please set data-category on sms-container");
        return;
    }

    loadMessages(category);
});
