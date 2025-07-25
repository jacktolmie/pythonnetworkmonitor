from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
import json
from modules.ping_node import get_results # For one-off pings
from modules.save_ping_results import save_ping_results # For one-off pings, or if you modify its use
from .models import Host, PingHost
from django.db import transaction

# For your API views, consider using Django Rest Framework for a more robust API.
# But for now, let's adapt your existing structure.

def index(request):
    return render(request, 'index.html')


@method_decorator(csrf_exempt, name='dispatch') # For simplicity in this example, but use proper CSRF handling
class PingAPIView(View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            host_address = data.get('host')
            num_pings = data.get('num_pings', 5)

            if not host_address:
                return JsonResponse({'success': False, 'error': 'Host address is required.'}, status=400)

            output, success = get_results(host_address, num_pings)

            # You might want to save one-off ping results too, but it's optional.
            # If you want to save, you'll need to pass correct data to save_ping_results
            # For this example, we just return the output.

            return JsonResponse({
                'success': True,
                'output': output,
                'ping_successful': success
            })
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON.'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)


@method_decorator(csrf_exempt, name='dispatch')
class AddMonitorTargetAPIView(View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            hostname = data.get('host')
            host_ip = data.get('host_ip')
            description = data.get('description', '')

            if not hostname or not host_ip:
                return JsonResponse({'success': False, 'message': 'Host name and IP/Hostname are required.'}, status=400)

            try:
                with transaction.atomic():
                    host, created = Host.objects.get_or_create(
                        name=hostname,
                        defaults={'ip_address': host_ip, 'description': description, 'is_active': True, 'ping_interval': 1}
                    )
                    if not created:
                        # If host already exists, ensure it's active and update description/IP if needed
                        if host.ip_address != host_ip:
                            host.ip_address = host_ip
                        if host.description != description:
                            host.description = description
                        host.is_active = True # Ensure it's active if re-added
                        host.save() # This save will trigger the Celery periodic task update
                        return JsonResponse({'success': True, 'message': f'Host {hostname} updated and monitoring ensured.'})
                    else:
                        host.save() # This save will trigger the Celery periodic task creation
                        return JsonResponse({'success': True, 'message': f'Host {hostname} added to monitoring.'})

            except Exception as e:
                # Handle specific DB errors or validation if needed
                return JsonResponse({'success': False, 'message': f'Database error: {e}'}, status=500)

        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Invalid JSON.'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'An unexpected error occurred: {e}'}, status=500)


@method_decorator(csrf_exempt, name='dispatch')
class UpdateFrequencyAPIView(View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            host_id = data.get('id')
            frequency = data.get('frequency')

            if not host_id or not frequency:
                return JsonResponse({'success': False, 'error': 'Host ID and frequency are required.'}, status=400)

            try:
                host = Host.objects.get(id=host_id)
                host.ping_interval = int(frequency)
                host.save() # This will trigger the save method, which updates the PeriodicTask
                return JsonResponse({'success': True, 'message': f'Ping frequency updated for {host.name} to {frequency} minutes.'})
            except Host.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Host not found.'}, status=404)
            except ValueError:
                return JsonResponse({'success': False, 'error': 'Invalid frequency value.'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON.'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)


@method_decorator(csrf_exempt, name='dispatch')
class DeleteTargetAPIView(View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            host_id = data.get('id')

            if not host_id:
                return JsonResponse({'success': False, 'message': 'Host ID is required.'}, status=400)

            try:
                host = Host.objects.get(id=host_id)
                host_name = host.name
                host.delete() # This will trigger the delete method, which deletes the PeriodicTask
                return JsonResponse({'success': True, 'message': f'Host {host_name} and its monitoring removed.'})
            except Host.DoesNotExist:
                return JsonResponse({'success': False, 'message': 'Host not found.'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Invalid JSON.'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'An unexpected error occurred: {e}'}, status=500)


@method_decorator(csrf_exempt, name='dispatch')
class ListHostsAPIView(View):
    def get(self, request, *args, **kwargs):
        hosts = Host.objects.all().order_by('name')
        hosts_data = []
        for host in hosts:
            last_ping_result = host.ping_results.first() # Get the most recent ping result
            hosts_data.append({
                'id': host.id,
                'name': host.name,
                'ip_address': host.ip_address,
                'description': host.description,
                'is_active': host.is_active,
                'added_date': host.added_date.isoformat(),
                'ping_interval': host.ping_interval,
                'last_checked': last_ping_result.timestamp.isoformat() if last_ping_result else None,
                'last_downtime': last_ping_result.last_downtime.isoformat() if last_ping_result and not last_ping_result.was_successful else None,
                # For display in frontend
                'is_hostname': host.name, # Using 'name' for display
                'resolved_ip': host.ip_address # Using 'ip_address' for resolved IP display
            })
        return JsonResponse({'hosts': hosts_data})
