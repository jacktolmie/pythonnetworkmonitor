import json
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_POST

from modules import ping_node

def api_ping_host(request):
    try:
        data = json.loads(request.body)
        host = data.get('host')
        num_pings = data.get('num_pings', 5)
    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON")

    if not host:
        return HttpResponseBadRequest("Host parameter is required.")

    ping_result = ping_node.ping_node(host, num_pings)
    ping_successful = not ("Could not" in ping_result)

    return JsonResponse({
        'success': True,
        'host': host,
        'output': ping_result,
        'ping_successful': ping_successful
    })