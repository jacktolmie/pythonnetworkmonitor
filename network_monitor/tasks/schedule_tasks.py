# network_monitor/tasks/schedule_tasks.py
from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from network_monitor.models import Host, PingHost

# Import the specific task from the other file within the tasks package
from .ping_tasks import ping_single_host

@shared_task
def ping_hosts():
    now = timezone.now()
    active_hosts = Host.objects.filter(is_active=True)

    for host in active_hosts:
        if host.last_ping_time:
            time_since_last_ping = now - host.last_ping_time
            if time_since_last_ping.total_seconds() >= host.ping_interval:
                print(f"Host {host.name} is due for a ping. Scheduling task...")
                ping_single_host.delay(host.name)
            else:
                remaining_time = host.ping_interval - time_since_last_ping.total_seconds()

        else:
            print(f"Host {host.name} never pinged. Scheduling initial ping...")
            ping_single_host.delay(host.name)