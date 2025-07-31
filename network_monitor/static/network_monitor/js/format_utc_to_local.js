// This function converts an iso time to a more readable one.
// In the form of: Jul 30, 2025, 15:43
export function formatUtcToLocal(isoString) {
    if (!isoString) return 'N/A';
    try {
        const date = new Date(isoString);
        const options = {
            month: 'short',
            day: '2-digit',
            year: 'numeric',
            hour: '2-digit',
            minute: '2-digit',
            hour12: false,
        };

        return date.toLocaleString(undefined, options);

    } catch (e) {
        console.error("Error parsing date:", isoString, e);
        return 'Invalid Date';
    }
}