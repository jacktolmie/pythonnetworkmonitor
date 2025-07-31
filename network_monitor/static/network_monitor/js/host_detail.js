import {utilsFormatUtcToLocal, utilsDisplayUpdateMessage, getCsrfToken, utilsGetDuration} from "./utils.js";

const {short_duration: message_display_duration_short, long_duration: message_display_duration_long, fade_duration: message_fade_duration} = utilsGetDuration();

// Function to update ping frequency (sends POST request to Django backend)
async function updatePingFrequency(hostId, frequency) {

    utilsDisplayUpdateMessage(
        'update-message',
        'Updating interval...',
        false,
        message_display_duration_short
    );

    try {
        const response = await fetch('/monitor/api/update_frequency/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken()
            },
            body: JSON.stringify({id: hostId, frequency: frequency})
        });
        const data = await response.json();
        if (response.ok && data.success) {
            utilsDisplayUpdateMessage(
                'update-message',
                data.message,
                false,
                message_display_duration_short
            );
        } else {
            const errorMessage = data.error || `Failed with status: ${response.status}`;
            utilsDisplayUpdateMessage(
                'update-message',
                `Failed to update: ${errorMessage}`,
                true,
                message_display_duration_long
            );
        }
    } catch (error) {
        utilsDisplayUpdateMessage(
            'update-message',
            `An error occurred: ${error.message}`,
            true,
            message_display_duration_long
        );
    }
}

// --- Main DOMContentLoaded Listener ---
document.addEventListener('DOMContentLoaded', function () {
    const pingIntervalSelect = document.getElementById('ping-interval-select');

    if (pingIntervalSelect) {
        pingIntervalSelect.onchange = async (event) => {
            const hostId = event.target.dataset.hostId;
            const frequency = event.target.value;
            await updatePingFrequency(hostId, frequency);
        };
    }

    // Loops through all .js-local-datetime elements, and passes them onto the utilsFormatUtcToLocal.js file.
    document.querySelectorAll('.js-local-datetime').forEach(element => {
        const utcString = element.dataset.utcDatetime; // Get the UTC date string
        element.textContent = utilsFormatUtcToLocal(utcString); // Format and display
    });
});
