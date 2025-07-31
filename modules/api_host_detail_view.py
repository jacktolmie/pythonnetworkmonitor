from django.db.models import Sum, Avg
from django.shortcuts import render, get_object_or_404

from modules.time_format import format_timedelta_to_hms
from network_monitor.models import Host, PingHost, HostDowntimeEvent

def api_host_detail_view(request, host_id):
    host = get_object_or_404(Host, pk=host_id)

    # --- Fetching Ping Statistics ---
    # Get recent ping results (e.g., last 24 hours or last 100 pings)
    # You might want to pass a 'period' parameter from the frontend later
    recent_pings = PingHost.objects.filter(host=host).order_by('-timestamp')[:10] # Last 10 pings

    # Convert timestamps to iso format to be converted by format_utc_to_local.js
    for ping in recent_pings:
        ping.timestamp = ping.timestamp.isoformat()

    if host.added_date:
        host.added_date = host.added_date.isoformat()

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
    formatted_total_duration = format_timedelta_to_hms(total_downtime_duration)

    # List of recent downtime events
    # recent_downtime_events = HostDowntimeEvent.objects.filter(host=host).order_by('-start_time')[:10] # Last 10 events
    recent_downtime_events = HostDowntimeEvent.objects.filter(host=host).order_by('-start_time')[:10]
    recent_downtime_events_data = []

    for event in recent_downtime_events:
        # Format individual event duration using the helper function
        formatted_event_duration = format_timedelta_to_hms(event.duration) if event.duration else "(Still Down)"

        recent_downtime_events_data.append(
            {
                'start_time': event.start_time.isoformat(),
                'end_time': event.end_time.isoformat() if event.end_time else None,
                'duration': formatted_event_duration,
            }
        )
    context = {
        'host': host,
        'avg_ping_speed': f"{avg_ping_speed:.2f} ms" if avg_ping_speed is not None else "N/A",
        'total_downtime_events': total_downtime_events,
        'total_downtime_duration': formatted_total_duration,
        'recent_pings': recent_pings,
        'recent_downtime_events_data': recent_downtime_events_data,
    }
    # print(context)
    return render(request, 'network_monitor/host_detail.html', context)