import json

from django.http import HttpResponseBadRequest, JsonResponse
from modules import get_host_info

def api_add_monitor(request):

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

    # Check result[0] ('success' or 'failure') for result of trying to add host.
    if result[0] == 'success':
        return JsonResponse({
            'success': True,
            'message': result[1]
        })
    else:
        return JsonResponse({
            'success': False,
            'message': result[1]
        })