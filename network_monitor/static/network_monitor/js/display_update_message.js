// This function displays the sent message to the object ID from the sender.

import { utilsGetDuration } from './utils.js'
export function displayUpdateMessage(send_element, message, isError = false, duration = 3000) {

    const { message_display_duration_short, message_display_duration_long, message_fade_duration } = utilsGetDuration();
    const elementId = document.getElementById(send_element);

    // Exit the function if element doesn't exist
    if (!elementId) {
        console.error(`Error: Element with ID '${elementId}' not found for message display.`);
        return;
    }
    // Clear any existing timeouts to prevent conflicts if a new message comes in
    if (elementId._messageTimeout) {
        clearTimeout(elementId._messageTimeout);
        elementId._messageTimeout = null;
    }

    // Set the message and styling
    elementId.textContent =     message;
    elementId.className =       `text-sm mt-2 ${isError ? 'text-red-600' : 'text-green-600'} show`;
    elementId.style.display =   'block'; // Ensure it's visible

    // Set a timeout to start clearing/fading the message
    elementId._messageTimeout = setTimeout(() => {
        elementId.classList.remove('show'); // Start fade out

        // After fadeDuration (0.5s from CSS), clear content and hide completely
        setTimeout(() => {
            elementId.textContent =     '';
            elementId.className =       `text-sm mt-2`; // Reset to base classes if any
            elementId.style.display =   'none';
        }, message_fade_duration); // This should match your CSS transition duration for opacity
    }, duration);
}