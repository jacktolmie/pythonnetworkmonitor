import json
from django.http import JsonResponse, HttpResponseBadRequest, HttpRequest

from modules import ping_node
from network_monitor.models import Host


def api_ping_host(request):

    num_pings = None
    host = None
    if isinstance(request, HttpRequest):
        try:
            data = json.loads(request.body)
            host = data.get('host')
            num_pings = data.get('num_pings', 5)

        except json.JSONDecodeError:
            return HttpResponseBadRequest("Invalid JSON")

        if not host:
            return HttpResponseBadRequest("Host parameter is required.")

    elif isinstance(request, int):
        host = Host.objects.get(id=request).ip_address
        num_pings = 5
    else:
        raise TypeError(f"Unsupported input type: {type(request).__name__}")

    ping_result = ping_node.ping_node(host, num_pings)
    ping_successful = not ("Could not" in ping_result)
    return JsonResponse({
        'success': ping_successful,
        'host': host,
        'output': ping_result,
        'ping_successful': ping_successful
    })