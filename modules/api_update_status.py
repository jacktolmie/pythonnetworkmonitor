import json
from django.http import JsonResponse, HttpResponseBadRequest
from network_monitor.models import Host

def api_update_status(request):
    try:
        data = json.loads(request.body)
        print(data)
        hostname = Host.objects.get(id = data['id'])
        hostname.is_active = True if data.get('is_active') == 'active' else False
        print("Is host active? ", hostname.is_active)
        hostname.save(update_fields=['is_active'])

        return JsonResponse({
            'success': True,
            'message': f"Host is now {"active" if hostname.is_active else "inactive"}"
        })
    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON")
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        })