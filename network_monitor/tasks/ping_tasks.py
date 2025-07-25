# network_monitor/tasks/ping_tasks.py
from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from network_monitor.models import Host, PingHost, HostDowntimeEvent # Use full path if needed, or relative import

@shared_task
def ping_single_host(host_id):
    try:
        host = Host.objects.get(id=host_id)
        if not host.is_active:
            print(f"Host {host.name} is inactive. Skipping ping.")
            return

        target = host.ip_address if host.ip_address else host.name
        print(f"Initiating ping for host: {host.name} ({target})")

        ping_result_data = pingget_ping(target)
        ping_successful = ping_result_data.get('status') == 'success'

        PingHost.objects.create(
            host=host,
            min_rtt=ping_result_data.get('min_rtt'),
            max_rtt=ping_result_data.get('max_rtt'),
            avg_rtt=ping_result_data.get('latency_ms'),
            packet_loss=ping_result_data.get('packet_loss'),
            was_successful=ping_successful,
            timestamp=timezone.now()
        )

        if ping_successful:
            host.last_ping_time = timezone.now()
            if host.is_currently_down:
                active_downtime = HostDowntimeEvent.objects.filter(host=host, end_time__isnull=True).order_by('-start_time').first()
                if active_downtime:
                    active_downtime.end_time = timezone.now()
                    active_downtime.save()
                    print(f"Host {host.name} is back up. Downtime ended at {active_downtime.end_time}")
                host.is_currently_down = False
            host.save()
            print(f"Successfully pinged {host.name} at {host.last_ping_time}")
        else:
            print(f"Failed to ping {host.name}. Result: {ping_result_data}")
            if not host.is_currently_down:
                HostDowntimeEvent.objects.create(host=host, start_time=timezone.now())
                host.is_currently_down = True
                print(f"Host {host.name} is now down. Downtime started.")
            host.save()

    except Host.DoesNotExist:
        print(f"Host with ID {host_id} does not exist.")
    except Exception as e:
        print(f"An error occurred while pinging host {host_id}: {e}")