from django.db.models import Sum, Avg
from django.shortcuts import render, get_object_or_404

from modules.get_ping_downtime_data import get_ping_downtime_data
from modules.time_format import format_timedelta_to_hms
from network_monitor.models import Host, PingHost, HostDowntimeEvent

def api_host_detail_view(request, host_id):
    host = get_object_or_404(Host, pk=host_id)

    # Get ping data from get_ping_downtime_data function
    get_ping_data = get_ping_downtime_data(host, "PingHost")
    recent_pings = get_ping_data["recent_pings"]
    avg_ping_speed = get_ping_data["avg_ping_speed"]

    # Get downtime data from get_ping_downtime_data function
    get_downtime_data = get_ping_downtime_data(host_id, "HostDowntimeEvent")
    recent_downtime_events_data = get_downtime_data["recent_downtime_events_data"]
    formatted_total_duration = get_downtime_data["formatted_total_duration"]
    total_downtime_events = get_downtime_data["total_downtime_events"]

    context = {
        'host': host,
        'avg_ping_speed': f"{avg_ping_speed:.2f} ms" if avg_ping_speed is not None else "N/A",
        'total_downtime_events': total_downtime_events,
        'total_downtime_duration': formatted_total_duration,
        'recent_pings': recent_pings,
        'recent_downtime_events_data': recent_downtime_events_data,
    }

    return render(request, 'network_monitor/host_detail.html', context)