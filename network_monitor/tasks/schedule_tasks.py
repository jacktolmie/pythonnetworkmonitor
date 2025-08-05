# network_monitor/tasks/schedule_tasks.py
from celery import shared_task
from django.utils import timezone

from network_monitor.models import Host
from network_monitor.tasks.ping_tasks import ping_single_host
from modules.get_host_info import get_host_info

@shared_task
def ping_hosts():
    now = timezone.now()
    active_hosts = Host.objects.filter(is_active=True)

    for host in active_hosts:
        if host.last_ping_attempt:
            time_since_last_ping = now - host.last_ping_attempt
            if time_since_last_ping.total_seconds() >= host.ping_interval:
                print(f"Host {host.name} is due for a ping. Scheduling task...")
                get_host_info.delay(hostname= host.name, host_ip=host.ip_address, description=host.description , save=True, num_pings=2)

        else:
            print(f"Host {host.name} never pinged. Scheduling initial ping...")
            ping_single_host.delay(host.name)