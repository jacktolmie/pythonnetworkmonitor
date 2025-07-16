import json
from django.shortcuts import render
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import csrf_exempt # Be careful with csrf_exempt in production!
from django.utils import timezone

from modules.get_host_info import get_host_info
from modules.pingnode import *

# Create your views here.

# Web page.
def index(request):
    return render(request, 'network_monitor/index.html')

# Retrieves the data from the host. Inputs will include the host,
# number of pings (defaults to 5), and if it should be monitored.
@require_POST
def ping_host_api(request):
    try:
        data =      json.loads(request.body)
        host =      data['host']
        num_pings = data.get('num_pings', 5)
    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON")

    if not host:
        return HttpResponseBadRequest("Host parameter is required.")

    ping_result = ping_node(host, num_pings)
    ping_successful = not("Could not" in ping_result)

    return JsonResponse({
        'success': True,
        'host': host,
        'output': ping_result,
        'ping_successful': ping_successful
    })

# Returns a list of monitored hosts.
@require_GET
def get_monitored_hosts_api(request):
    hosts_data = []

# Adds a new target to be monitored.
# Uses get_host_info with save=True.
@csrf_exempt # For simplicity in development, but consider CSRF tokens for production!
@require_POST
def add_monitor_target_api(request):

    try:
        data = json.loads(request.body)
        host_input =    data.get('host')
        num_pings =     data.get('num_pings', 5)
        hostname =      data.get('hostname')
        host_ip =       data.get('host_ip')
    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON")

    if not host_input:
        return HttpResponseBadRequest("Host parameter is required.")

    # Call get_host_info with save=True to handle validation, ping, and DB interaction
    result = get_host_info(hostname, host_ip, save=True, num_pings=num_pings)

    if result['success']:
        return JsonResponse(result) # result already contains success, message, target
    else:
        return JsonResponse(result, status=400) # Return appropriate status for failure

