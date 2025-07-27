from django.http import JsonResponse
from modules import get_host_info
from network_monitor.models import PingHost, Host

def api_get_monitored_hosts(request):
    hosts_data = []
    check_host = lambda target_host: PingHost.objects.filter(host_id = target_host).order_by('-timestamp').first()

    for target in Host.objects.all().order_by('name'):
        latest_ping_result = check_host(target)

        # If the host has no ping data, ping host and save data.
        if not latest_ping_result:
            get_host_info.get_host_info(hostname=target.name, host_ip=target.ip_address, save=True, num_pings=1)
            latest_ping_result = check_host(target)

        # Add info for full monitoring webpage for each node.
        hosts_data.append({
            'id': target.id,
            'target_string': target.description,
            'resolved_ip': target.ip_address,
            'hostname': target.name,
            'is_active': target.is_active,
            'ping_interval': target.ping_interval,
            'last_checked': latest_ping_result.timestamp.isoformat(),
            'last_downtime': target.last_down_time.isoformat() if target.last_down_time else None,
            'is_currently_down' : target.is_currently_down
        })

    return JsonResponse({'hosts': hosts_data})