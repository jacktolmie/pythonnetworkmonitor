from django import template
from datetime import timedelta

register = template.Library()

# Formats a timedelta object for shorter display (e.g., 1h 2m 3s).
# Omits parts that are zero (e.g., "5m" instead of "0h 5m 0s").

@register.filter
def format_duration(td):

    if not isinstance(td, timedelta):
        return td

    total_seconds = int(td.total_seconds())
    if total_seconds == 0:
        return "0s"

    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    parts = []
    if hours > 0:
        parts.append(f"{hours}h")
    if minutes > 0:
        parts.append(f"{minutes}m")
    if seconds > 0 or (not parts and total_seconds == 0): # Ensure "0s" is shown if duration is 0
        parts.append(f"{seconds}s")

    return " ".join(parts) if parts else "0s" # Fallback for very small durations if all parts are 0