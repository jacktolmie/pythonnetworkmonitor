import json
from django.http import JsonResponse, HttpResponseBadRequest
from network_monitor.models import Host

def api_update_ping_frequency(request):

    try:
        data =                  json.loads(request.body)
        hostname =              Host.objects.get(id = data['id'])
        hostname.ping_interval =int(data.get('frequency') if data.get('frequency') else 1)
        hostname.save(update_fields=['ping_interval'])

        return JsonResponse({
            'success': True,
            'message': f"Ping frequency for {hostname.name} updated to {hostname.ping_interval} minutes."
        })

    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON")
    except ValueError:
        return JsonResponse({'success': False, 'error': 'Frequency must be an integer.'}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)
