# pythonnetworkmonitor/network_monitor/apps.py

from django.apps import AppConfig

# from tasks import schedule_tasks, cleanup_tasks, ping_tasks

class NetworkMonitorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'network_monitor'

    def ready(self):

        pass
