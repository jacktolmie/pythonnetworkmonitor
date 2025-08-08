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

async function deleteData(hostId, table, days, message) {
    
    utilsDisplayUpdateMessage(
        'delete-data-message',
        message,
        false,
        message_display_duration_short
    );

    try {
        const response = await fetch('/monitor/api/delete_host_data/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken()
            },
            body: JSON.stringify({host_id:hostId, database_name: table, days_old_max: days})
        });
        const data = await response.json();
        
        if (response.ok && data.success) {
            utilsDisplayUpdateMessage(
                'delete-data-message',
                `Deleted ${data.total_deleted} rows.`,
                false,
                message_display_duration_short
            );
            // Refresh the page to re-fetch updated ping/downtime data from the backend.
            // The backend host detail view calls get_ping_downtime_data() to prepare fresh data.
            setTimeout(() => {
                window.location.reload();
            }, 500);
        } else {
            const errorMessage = data.error || `Failed with status: ${response.status}`;
            utilsDisplayUpdateMessage(
                'delete-data-message',
                `Failed to update: ${errorMessage}`,
                true,
                message_display_duration_long
            );
        }
    } catch (error) {
        utilsDisplayUpdateMessage(
            'delete-data-message',
            `An error occurred: ${error.message}`,
            true,
            message_display_duration_long
        );
    }

}

async function updateMonitoredStatus(hostId, active)    {

    utilsDisplayUpdateMessage(
        'update_status',
        'Updating Monitored Status...',
        false,
        message_display_duration_short
    );

    try {
        const response = await fetch('/monitor/api/update_status/', {
           method: 'POST',
           headers: {
               'Content-Type': 'application/json',
               'X-CSRFToken': getCsrfToken()
           },
            body: JSON.stringify({id:hostId, is_active:active})
        });
        console.log(response)
        const data = await response.json();

        if (response.ok && data.success) {
            utilsDisplayUpdateMessage(
              'update_status',
              'Updated Monitored Status',
              false,
              message_display_duration_short
            );
        }
        else {
            const errorMessage = data.error || `Failed to update Monitored Status: ${response.status}`;
            utilsDisplayUpdateMessage(
                'update_status',
                `An error occurred: ${errorMessage}`,
                true,
                message_display_duration_long
            );
        }
    }
    catch(error) {
        utilsDisplayUpdateMessage(
            'update_status',
            `An error occurred: ${error.message}`,
            true,
            message_display_duration_long
        );
    }

}

function handleEnterKeyPress(event, buttonToClick) {
    if(event.key === "Enter") {
        event.preventDefault();
        buttonToClick.click();
    }
}



// --- Main DOMContentLoaded Listener ---
document.addEventListener('DOMContentLoaded', function () {

    // Change activated/deactivated status
    const  isActive = document.getElementById('is_active');

    if (isActive) {
        isActive.onchange = async (event) => {
            const hostId = event.target.dataset.hostId;
            const active = event.target.value;
            await updateMonitoredStatus(hostId, active);
        }
    }

    // Change ping interval
    const pingIntervalSelect = document.getElementById('ping-interval-select');

    if (pingIntervalSelect) {
        pingIntervalSelect.onchange = async (event) => {
            const hostId = event.target.dataset.hostId;
            const frequency = event.target.value;
            await updatePingFrequency(hostId, frequency);
        };
    }

    // Get information about number of days to remove from PingHost data table.
    const deletePingButton = document.getElementById('ping_delete_days_button');
    const deletePingDays = document.getElementById('ping_delete_days');

    if (deletePingDays && deletePingButton) {
        deletePingDays.addEventListener('keydown', (event) => handleEnterKeyPress(event, deletePingButton));
    }

    deletePingButton.addEventListener('click', async(event) => {
        const hostId = event.target.dataset.hostId;
        const hostName = event.target.dataset.hostName;
        const daysToDelete = deletePingDays.value;
        await deleteData(hostId, 'PingHost', daysToDelete, `Deleting ${daysToDelete} days from ${hostName}`)

    })

    // Get information about number of days to remove from HostDowntimeEvent data table.
    const deleteDowntimeButton = document.getElementById('downtime_delete_days_button');
    const deleteDowntimeDays = document.getElementById('downtime_delete_days');

    if (deleteDowntimeDays && deleteDowntimeButton) {
        deleteDowntimeDays.addEventListener('keydown', (event) => {handleEnterKeyPress(event, deleteDowntimeButton)})
    }

    deleteDowntimeButton.addEventListener('click', async(event) => {
        const hostId = event.target.dataset.hostId;
        const hostName = event.target.dataset.hostName;
        const daysToDelete = deleteDowntimeDays.value;
        await deleteData(hostId, "HostDowntimeEvent", daysToDelete, `Deleting ${daysToDelete} days from ${hostName}`);
    });

    // Loops through all .js-local-datetime elements, and passes them onto the utilsFormatUtcToLocal.js file.
    document.querySelectorAll('.js-local-datetime').forEach(element => {
        const utcString = element.dataset.utcDatetime; // Get the UTC date string
        element.textContent = utilsFormatUtcToLocal(utcString); // Format and display
    });
});
