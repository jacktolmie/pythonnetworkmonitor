# network_monitor/tasks/__init__.py

from network_monitor.tasks.ping_tasks import ping_single_host
from network_monitor.tasks.schedule_tasks import ping_hosts
from network_monitor.tasks.cleanup_tasks import delete_old_data
