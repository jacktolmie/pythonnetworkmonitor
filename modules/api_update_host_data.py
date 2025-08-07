import json
from django.http import JsonResponse
from modules.get_ping_downtime_data import get_ping_downtime_data

def api_update_host_data(request):

    try:
        data = json.loads(request.body)
        host_id = data.get('host_id')
        table_name = data.get('table_name')


        return JsonResponse({

        })