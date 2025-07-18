import json
from django.shortcuts import render
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import csrf_exempt # Be careful with csrf_exempt in production!
from django.utils import timezone

from modules import get_host_info, pingnode
from modules.save_ping_results import save_ping_results
from .models import Host, PingHost


# Web page.
def index(request):
    return render(request, 'network_monitor/index.html')

# Retrieves the data from the host. Inputs will include the host,
# number of pings (defaults to 5), and if it should be monitored.
@csrf_exempt
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

    ping_result =       pingnode.ping_node(host, num_pings)
    ping_successful =   not("Could not" in ping_result)

    return JsonResponse({
        'success': True,
        'host': host,
        'output': ping_result,
        'ping_successful': ping_successful
    })

# Returns a list of monitored hosts.
@csrf_exempt
@require_GET
def get_monitored_hosts_api(request):
    hosts_data = []
    for target in Host.objects.all().order_by('name'):
        latest_ping_result = PingHost.objects.filter(host_id = target).order_by('-timestamp').first()
        hosts_data.append({
            'id': target.name,
            'target_string': target.description,
            'resolved_ip': target.ip_address,
            'is_hostname': target.name,
            'is_active': target.is_active,
            'last_checked': latest_ping_result.timestamp.isoformat(),
            'last_downtime': latest_ping_result.last_downtime.isoformat() if latest_ping_result.last_downtime else None,
        })

    return JsonResponse({'hosts': hosts_data})

# Adds a new target to be monitored.
# Uses get_host_info with save=True.
@csrf_exempt # For simplicity in development, but consider CSRF tokens for production!
@require_POST
def add_monitor_target_api(request):
    try:
        data =          json.loads(request.body)
        host_input =    data.get('host')
        host_ip =       data.get('host_ip')
        description =   data.get('description')

    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON")

    if not host_input:
        return HttpResponseBadRequest("Host parameter is required.")

    # Call get_host_info with save=True to handle validation, ping, and DB interaction
    result = get_host_info.get_host_info(hostname= host_input, host_ip= host_ip, save= True, num_pings= 2)

    if result == 'success':
        return JsonResponse({
            'success': True,
            'message': result[1]
        })
    else:
        return JsonResponse({
            'success': False,
            'message': result[1]
        })

@csrf_exempt
@require_POST
def delete_monitor_target_api(request):
    try:
        data = json.loads(request.body)
        get_host_obj = Host.objects.get(name = data['id'])
        deleted_host, details = get_host_obj.delete()
        return JsonResponse({
            'success': True,
            'message': f"{deleted_host} has been deleted."
        })
    except Host.DoesNotExist:
        print(f"Does not exist")
        return JsonResponse({
            'success': False,
            'message': f"does not exist."
        })
    except Exception as e:
        print(f"Who knows how to delete: {e}")
        return JsonResponse({
            'success': False,
            'message': f"{e}"
        })