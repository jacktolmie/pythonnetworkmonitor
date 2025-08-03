import { utilsFormatUtcToLocal, utilsDisplayUpdateMessage, getCsrfToken, utilsGetDuration} from "./utils.js";
import { refresh_monitored_list } from "./constants.js";

// Get message display and fade durations.
const {short_duration: message_display_duration_short, long_duration: message_display_duration_long, fade_duration: message_fade_duration} = utilsGetDuration();

// --- Enter Key Press Handler ---
function handleEnterKeyPress(event, buttonToClick) {
    if (event.key === 'Enter') {
        event.preventDefault(); // Prevent default form submission/line break
        buttonToClick.click();  // Programmatically click the associated button
    }
}

// --- Function to fetch and render monitored hosts ---
async function fetchAndRenderHosts() {
    const tableBody = document.getElementById('host-table-body');

    // Show loading message only if table is currently empty
    if (tableBody.children.length === 0 || tableBody.children[0].colSpan === 8) { // Updated colspan check
        tableBody.innerHTML = '<tr><td colspan="8" class="py-4 text-center text-gray-500">Loading monitored hosts...</td></tr>'; // Updated colspan
    }

    try {
        const response = await fetch('/monitor/api/hosts/'); // Your Django API URL
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json(); // Assuming your API returns { "hosts": [...] }

        tableBody.innerHTML = ''; // Clear existing rows

        if (data.host && data.host.length === 0) {
            tableBody.innerHTML = '<tr><td colspan="8" class="py-4 text-center text-gray-500">No hosts currently being monitored. Add one above!</td></tr>'; // Updated colspan
            return;
        }

        data.hosts.forEach(host => {
            const row = document.createElement('tr');
            row.className = 'border-b border-gray-200 hover:bg-gray-100';

            const statusClass = host.is_currently_down ? 'inactive' : 'active';

            row.innerHTML = `
                        <td class="py-3 px-6 text-left whitespace-nowrap">
                            <span class="status-light ${statusClass}"></span>
                            <span class="font-medium">${host.is_currently_down ? 'Offline' : 'Online'}</span>
                        </td>
                        <td class="py-3 px-6 text-center">
                            <strong><a href="/monitor/host/${host.hostname}/" class="text-blue-600 hover:underline">${host.hostname}</a></strong>
                        </td>
                        <td class="py-3 px-6 text-center">${host.resolved_ip || 'N/A'}</td>
                        <td class="py-3 px-6 text-center">${utilsFormatUtcToLocal(host.last_checked)}</td>
                        <td class="py-3 px-6 text-center">
                            <button data-host-id="${host.id}" class="btn-danger delete-btn">Delete</button>
                        </td>
                        <td class="py-3 px-6 text-center">
                            <a href="/monitor/host/${host.id}/" class="btn-secondary">View Stats</a>
                        </td>
                    `;
            tableBody.appendChild(row);
        });

        // Re-attach event listeners for dynamically added elements
        document.querySelectorAll('.delete-btn').forEach(button => {
            button.onclick = (event) => deleteMonitorTarget(event.target.dataset.hostId);
        });

    } catch (error) {
        tableBody.innerHTML = '<tr><td colspan="8" class="py-4 text-center text-red-500">Failed to load hosts. Please check console for details.</td></tr>'; // Updated colspan
    }
}

// Function to delete a monitored target (sends POST request to Django backend)
async function deleteMonitorTarget(hostId) {
    // Using a custom modal/dialog is recommended instead of confirm() in production
    if (!confirm('Are you sure you want to delete this monitored host?')) {
        return;
    }
    try {
        const response = await fetch('/monitor/api/delete_target/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken() // Include CSRF token
            },
            body: JSON.stringify({id: hostId})
        });
        const data = await response.json();
        if (data.success) {
            utilsDisplayUpdateMessage(
                'message-area',
                data.message,
                false,
                message_display_duration_short
            );
            await fetchAndRenderHosts(); // Re-fetch to update the list immediately
        } else {
            utilsDisplayUpdateMessage(
                'message-area',
                `Failed to delete target: ${data.message}`,
                true,
                message_display_duration_long
            );
        }
    } catch (error) {
        utilsDisplayUpdateMessage(
            'message-area',
            'An error occurred while deleting target.',
            true,
            message_display_duration_long
        );
    }
}

// --- Main DOMContentLoaded Listener ---
document.addEventListener('DOMContentLoaded', async function () {

    // Get ping only textbox elements.
    const pingHostInput = document.getElementById('pingHostInput');
    const num_pings = document.getElementById('num_pings');
    const pingButton = document.getElementById('pingButton');
    const pingOutput = document.getElementById('pingOutput');
    pingOutput.textContent = "Awaiting ping request";
    const clearButton = document.getElementById('pingClearButton');

    // Get Add Monitor textbox elements.
    const hostname = document.getElementById('hostname');
    const host_ip = document.getElementById('host_ip');
    const description = document.getElementById('description');
    const addMonitorButton = document.getElementById('addMonitorButton');

    // Attach Enter key event listeners
    if (pingHostInput && num_pings && pingButton) {
        pingHostInput.addEventListener('keydown', (event) => handleEnterKeyPress(event, pingButton));
        num_pings.addEventListener('keydown', (event) => handleEnterKeyPress(event, pingButton));
    }

    if (hostname && host_ip && description && addMonitorButton) {
        hostname.addEventListener('keydown', (event) => handleEnterKeyPress(event, addMonitorButton));
        host_ip.addEventListener('keydown', (event) => handleEnterKeyPress(event, addMonitorButton));
        description.addEventListener('keydown', (event) => handleEnterKeyPress(event, addMonitorButton));
    }

    // Event Listener for Ping Button (one-off ping)
    pingButton.addEventListener('click', async () => {
        const host = pingHostInput.value.trim();
        const pingOutputDiv = document.getElementById('pingOutput');
        const numPings = parseInt(num_pings.value.trim() || '5');

        if (isNaN(numPings) || numPings < 1) {
            pingOutputDiv.textContent = "Please insert a valid number of pings (e.g., 1 or more).";
            pingOutputDiv.className = 'ping-output-box p-4 text-sm text-red-500';
            return;
        }

        if (!host) {
            pingOutputDiv.textContent = 'Please enter a host to ping.';
            pingOutputDiv.className = 'ping-output-box p-4 text-sm text-red-500';
            return;
        }

        pingOutputDiv.textContent = `Pinging ${host}... Please wait.`;
        pingOutputDiv.className = 'ping-output-box p-4 text-sm text-yellow-400';

        try {
            const response = await fetch('/monitor/api/ping/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCsrfToken() // Include CSRF token
                },
                body: JSON.stringify({host: host, num_pings: numPings})
            });
            const data = await response.json();

            if (data.success) {
                pingOutputDiv.textContent = data.output || 'No output received.';
                pingOutputDiv.className = `ping-output-box p-4 text-sm ${data.ping_successful ? 'text-green-400' : 'text-red-400'}`;
                pingHostInput.value = "";
                num_pings.value = "";
                if (data.error) {
                    pingOutputDiv.textContent += `\nError: ${data.error}`;
                }
                document.getElementById('pingClearButton').style.display = 'block';
            } else {
                pingOutputDiv.textContent = `Error: ${data.error}`;
                pingOutputDiv.className = 'ping-output-box p-4 text-sm text-red-500';
            }
        } catch (error) {
            pingOutputDiv.textContent = `An error occurred: ${error.message}`;
            pingOutputDiv.className = 'ping-output-box p-4 text-sm text-red-500';
        }
    });

    // Event Listener for Clear Output Button
    clearButton.addEventListener('click', async () => {
        pingOutput.textContent = 'Awaiting ping request';
        pingOutput.classList.remove('text-red-600');
        pingOutput.classList.add('text-green-600');
        document.getElementById('pingClearButton').style.display = 'none';
    });

    // Event Listener for Add Monitor Button
    addMonitorButton.addEventListener('click', async () => {

        const hostVal = hostname.value.trim();
        const hostIpVal = host_ip.value.trim();
        const hostDescriptionVal = description.value.trim();

        if (!hostVal || !hostIpVal) {
            utilsDisplayUpdateMessage(
                'message-area',
                "Please provide both a Host Name and an IP/Hostname to monitor.",
                true,
                message_display_duration_long);
            return;
        }

        utilsDisplayUpdateMessage(
            'message-area',
            'Adding host to monitoring...',
            false,
            message_display_duration_short
        );

        try {
            const response = await fetch('/monitor/api/add_target/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCsrfToken() // Include CSRF token
                },
                body: JSON.stringify({host: hostVal, host_ip: hostIpVal, description: hostDescriptionVal})
            });
            const data = await response.json();

            if (response.ok && data.success) { // Check response.ok for 2xx status codes
                utilsDisplayUpdateMessage(
                    'message-area',
                    data.message,
                    false,
                    message_display_duration_short
                );
                hostname.value = ""; // Clear inputs
                host_ip.value = "";
                description.value = "";
                await fetchAndRenderHosts(); // Refresh the list of monitored hosts
            } else {
                // Handle server-side validation errors or other non-200 responses
                const errorMessage = data.message || `Failed with status: ${response.status}`;
                utilsDisplayUpdateMessage(
                    'message-area',
                    `Error: ${errorMessage}`,
                    true,
                    message_display_duration_long
                );
            }
        } catch (error) {
            utilsDisplayUpdateMessage(
                'message-area',
                `An error occurred: ${error.message}`,
                true,
                message_display_duration_long
            );
        }
    });

    // Initial load of monitored hosts when the page loads
    await fetchAndRenderHosts();

    // Periodically refresh the monitored hosts list
    setInterval(fetchAndRenderHosts, refresh_monitored_list); // Set from constants.js file
});