import json

from django.db.models import Sum, Avg
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import get_object_or_404

from modules.time_format import format_timedelta_to_hms
from network_monitor.models import PingHost, HostDowntimeEvent

def get_ping_downtime_data(host_id, table_name) :

    # Get the ping results to display in host_detail.html.
    if table_name == "PingHost" :
        recent_pings = PingHost.objects.filter(host=host_id).order_by('-timestamp')

        # Convert timestamps to iso format to be converted by format_utc_to_local.js
        for ping in recent_pings:
            ping.timestamp = ping.timestamp.isoformat()

        if host_id.added_date:
            host_id.added_date = host_id.added_date.isoformat()

        # Calculate average ping speed (avg_rtt) for successful pings
        avg_ping_speed = PingHost.objects.filter(
            host=host_id,
            was_successful=True
        ).aggregate(
            avg_rtt=Avg('avg_rtt')
        )['avg_rtt']

        # return [recent_pings, avg_ping_speed]
        return {
            'recent_pings': recent_pings,
            'avg_ping_speed': avg_ping_speed
        }

    elif table_name == "HostDowntimeEvent" :

        # Total number of downtime events
        total_downtime_events = HostDowntimeEvent.objects.filter(host=host_id).count()

        # Total downtime duration (sum of ended events)
        total_downtime_duration = HostDowntimeEvent.objects.filter(
            host=host_id,
            end_time__isnull=False  # Only count ended events
        ).aggregate(
            total_duration=Sum('duration')
        )['total_duration']

        # Format total_downtime_duration for display
        formatted_total_duration = format_timedelta_to_hms(total_downtime_duration)

        # List of recent downtime events
        recent_downtime_events = HostDowntimeEvent.objects.filter(host=host_id).order_by('-start_time')
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

        # return [recent_downtime_events_data, formatted_total_duration, total_downtime_events]
        return {
            'total_downtime_events': total_downtime_events,
            'formatted_total_duration': formatted_total_duration,
            'recent_downtime_events_data': recent_downtime_events_data
        }
    else:
        return HttpResponseBadRequest("Invalid table name")