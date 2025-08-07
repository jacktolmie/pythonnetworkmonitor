// This is just to have a lot of functions bundled into a single file,
// to save adding a lot of them to the html files.

import { formatUtcToLocal } from './format_utc_to_local.js'
import { displayUpdateMessage } from './display_update_message.js'
import {getCssVariable, getDurations} from './get_css_variable.js'

export const utilsFormatUtcToLocal = (isoString) =>
    { return formatUtcToLocal(isoString) };

export const utilsDisplayUpdateMessage = (send_element, message, isError = false, duration = 3000) =>
    { return displayUpdateMessage(send_element, message, isError, duration) };

export const utilsGetDuration= () =>
    { return getDurations()}

// Get CSRF Token from meta tag
export function getCsrfToken() {
    return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
}