from django.db.models import Sum, Avg
from django.shortcuts import render, get_object_or_404
from network_monitor.models import Host, PingHost, HostDowntimeEvent

def api_host_detail_view(request, host_id):
    host = get_object_or_404(Host, pk=host_id)

    # --- Fetching Ping Statistics ---
    # Get recent ping results (e.g., last 24 hours or last 100 pings)
    # You might want to pass a 'period' parameter from the frontend later
    recent_pings = PingHost.objects.filter(host=host).order_by('-timestamp')[:100] # Last 100 pings

    # Calculate average ping speed (avg_rtt) for successful pings
    avg_ping_speed = PingHost.objects.filter(
        host=host,
        was_successful=True
    ).aggregate(
        avg_rtt=Avg('avg_rtt')
    )['avg_rtt']

    # --- Fetching Downtime Statistics ---
    # Total number of downtime events
    total_downtime_events = HostDowntimeEvent.objects.filter(host=host).count()

    # Total downtime duration (sum of ended events)
    total_downtime_duration = HostDowntimeEvent.objects.filter(
        host=host,
        end_time__isnull=False # Only count ended events
    ).aggregate(
        total_duration=Sum('duration')
    )['total_duration']

    # Format total_downtime_duration for display
    if total_downtime_duration:
        # total_seconds() returns float, convert to int for cleaner display
        total_downtime_seconds = int(total_downtime_duration.total_seconds())
        hours, remainder = divmod(total_downtime_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        formatted_duration = f"{hours}h {minutes}m {seconds}s"
    else:
        formatted_duration = "N/A"

    # List of recent downtime events
    recent_downtime_events = HostDowntimeEvent.objects.filter(host=host).order_by('-start_time')[:10] # Last 10 events

    context = {
        'host': host,
        'avg_ping_speed': f"{avg_ping_speed:.2f} ms" if avg_ping_speed is not None else "N/A",
        'total_downtime_events': total_downtime_events,
        'total_downtime_duration': formatted_duration,
        'recent_pings': recent_pings,
        'recent_downtime_events': recent_downtime_events,
    }
    return render(request, 'network_monitor/host_detail.html', context)