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
    check_host = lambda target: PingHost.objects.filter(host_id = target).order_by('-timestamp').first()

    for target in Host.objects.all().order_by('name'):
        latest_ping_result = check_host(target)

        # If the host has no ping data, ping host and save data.
        if not latest_ping_result:
            get_host_info.get_host_info(hostname=target.name, host_ip=target.ip_address,save=True, num_pings=1)
            latest_ping_result = check_host(target)

        hosts_data.append({
            'id': target.name,
            'target_string': target.description,
            'resolved_ip': target.ip_address,
            'is_hostname': target.name,
            'is_active': target.is_active,
            'ping_interval': latest_ping_result.ping_interval,
            'last_checked': latest_ping_result.timestamp.isoformat(),
            'last_downtime': latest_ping_result.last_downtime.isoformat() if latest_ping_result.last_downtime else None
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

    hostname = None
    try:
        data = json.loads(request.body)
        hostname = data.get('id')
        frequency = data.get('frequency')

        get_host_obj = Host.objects.get(name = hostname)
        deleted_host, details = get_host_obj.delete()

        return JsonResponse({
            'success': True,
            'message': f"{hostname} has been deleted."
        })
    except Host.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': f"{hostname} does not exist."
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f"Error deleting host: {e}"
        })

@csrf_exempt
@require_POST
def update_ping_frequency_api(request):
    try:
        data =                  json.loads(request.body)
        hostname =              PingHost.objects.get(host_id = Host.objects.get(name = data['id']))
        hostname.ping_interval =int(data.get('frequency') if data.get('frequency') else 1)
        hostname.save(update_fields=['ping_interval'])

        return JsonResponse({
            'success': True,
            'message': f"Ping frequency for {hostname.host} updated to {hostname.ping_interval} minutes."
        })

    except Host.objects.get(name = data['id']).DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Target not found.'}, status=404)
    except ValueError:
        return JsonResponse({'success': False, 'error': 'Frequency must be an integer.'}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON")