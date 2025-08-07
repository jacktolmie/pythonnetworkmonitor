import json
from django.http import JsonResponse, HttpResponseBadRequest, HttpRequest
from network_monitor.tasks.cleanup_tasks import delete_old_data

def api_delete_host_data(request):

    try:
        data = json.loads(request.body)
        host_id = data.get('host_id')
        database_name = data.get('database_name')
        days_old_max = data.get('days_old_max')

        return delete_old_data(host_id, database_name, days_old_max)

    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON")

