import json
from django.http import JsonResponse
from network_monitor.models import Host

def api_delete_monitor_target(request):

    host_name = "Node"
    try:
        data = json.loads(request.body)
        host_id = data.get('id')

        get_host_obj = Host.objects.get(id = host_id)
        host_name = get_host_obj.name

        # These variables are unused. Just keeping them if needed later.
        # This will delete the host from the database.
        deleted_host, details = get_host_obj.delete()

        return JsonResponse({
            'success': True,
            'message': f"{host_name} has been deleted."
        })
    except Host.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': f"{host_name} does not exist."
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f"Error deleting host: {e}"
        })