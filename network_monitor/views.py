from django.shortcuts import render
from django.views.decorators.http import require_POST, require_GET

from modules.api_add_monitor_target import api_add_monitor
from modules.api_delete_monitor_target import api_delete_monitor_target
from modules.api_get_monitored_host import api_get_monitored_hosts
from modules.api_host_detail_view import api_host_detail_view
from modules.api_ping_host import api_ping_host
from modules.api_update_ping_frequency import api_update_ping_frequency

# Adds a new target to be monitored.
# Uses get_host_info with save=True.
@require_POST
def add_monitor_target_api(request):
    return api_add_monitor(request)

# Delete the selected host.
@require_POST
def delete_monitor_target_api(request):
    return api_delete_monitor_target(request)

# Returns a list of monitored hosts.
@require_GET
def get_monitored_hosts_api(request):
    return api_get_monitored_hosts(request)

# Creates a webpage of the selecte host. Contains more data, and can make changes to it.
def host_detail_view_api(request, host_id):
    return api_host_detail_view(request, host_id)

# Web page.
def index(request):
    return render(request, 'network_monitor/index.html', {})

# Retrieves the data from the host. Inputs will include the host,
# number of pings (defaults to 5), and if it should be monitored.
@require_POST
def ping_host_api(request):
    return api_ping_host(request)

@require_POST
def update_ping_frequency_api(request):
    return api_update_ping_frequency(request)
