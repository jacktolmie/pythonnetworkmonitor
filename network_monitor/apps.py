# pythonnetworkmonitor/network_monitor/apps.py

from django.apps import AppConfig

# We still need this import for Celery to find our tasks.
# from . import tasks

class NetworkMonitorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'network_monitor'

    def ready(self):
        """
        The ready() method should be kept clean of database queries.
        It's now a placeholder, but could be used for other non-DB-related
        startup logic or to connect signals.
        """
        # The database setup logic has been moved to a management command.
        pass
