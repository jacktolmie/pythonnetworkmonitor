// This will get the variables from CSS files required to use in other js files.

export function getCssVariable(name) {

    name = name.trim()

    if (name.endsWith("ms")) {
        return parseFloat(name);
    }
    if (name.endsWith("s")) {
        return parseFloat(name) * 1000;
    }
    return parseFloat(name); // Assume milliseconds if no unit
}

export function getDurations() {
    const rootStyles = getComputedStyle(document.documentElement);

    return {
        short_duration: getCssVariable(rootStyles.getPropertyValue('--message-display-duration_short')),
        long_duration: getCssVariable(rootStyles.getPropertyValue('--message-display-duration_long')),
        fade_duration: getCssVariable(rootStyles.getPropertyValue('--message-fade-duration')),
    };
}