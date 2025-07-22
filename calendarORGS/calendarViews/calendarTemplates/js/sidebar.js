let eventDataDict = {};

async function loadEventData() {
    try {
        const response = await fetch('eventData.json');
        eventDataDict = await response.json();
    } catch (error) {
        console.error(error);
    }
}

document.addEventListener('DOMContentLoaded', loadEventData);

function openSidebar(eventId, eventColor) {
    const sidebar = document.getElementById("sidebar");
    const overlay = document.getElementById("sidebar-overlay");
    const content = document.getElementById("sidebar-content");
    const title = document.getElementById("sidebar-title");

    const data = eventDataDict[eventId];
    if (!data) {
        console.error(`No event data found for event ${eventId}`);
        return;
    }

    title.textContent = data.iD;
    content.innerHTML = `
    <div class="event-detail" style="border-left-color: ${eventColor};">
        <strong>Start:</strong> ${String(data.startParsed.dayOfWeek)}, ${data.startParsed.monthName}
                                ${String(data.startParsed.day)}, ${String(data.startParsed.year)}
                                ${data.endParsed.hrTime}
    </div>
    <div class="event-detail" style="border-left-color: ${eventColor};">
        <strong>End:</strong> ${String(data.endParsed.dayOfWeek)}, ${data.endParsed.monthName}
                                ${String(data.endParsed.day)}, ${String(data.endParsed.year)}
                                ${data.endParsed.hrTime}
    </div>
    <div class="event-detail" style="border-left-color: ${eventColor};">
        <strong>Description:</strong> ${data.description}
    </div>
    `;
    sidebar.classList.add("active");
    overlay.classList.add("active");
    document.body.classList.add('sidebar-open');
}

function closeSidebar() {
    const sidebar = document.getElementById("sidebar");
    const overlay = document.getElementById("sidebar-overlay");

    sidebar.classList.remove("active");
    overlay.classList.remove("active");
    document.body.classList.remove('sidebar-open');

    }

document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        closeSidebar();
    }
})