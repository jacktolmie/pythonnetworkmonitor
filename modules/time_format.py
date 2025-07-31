# Helper function to format timedelta (can be reused)
from datetime import timedelta


# Formats a timedelta object to HHh MMm SSs, omitting milliseconds.
# Returns "N/A" or "(Still Down)" for None/ongoing.
def format_timedelta_to_hms(td):

    if not isinstance(td, timedelta):
        return "(Still Down)" # Or "N/A" depending on context

    total_seconds = int(td.total_seconds())
    if total_seconds == 0 and td.total_seconds() == 0: # Check for exact zero timedelta
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

    return " ".join(parts) if parts else "0s"
