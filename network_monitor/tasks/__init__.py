# network_monitor/tasks/__init__.py

# from .ping_tasks import ping_single_host # Import the specific task
# from schedule_tasks import ping_hosts   # Import the specific task
# from ping_tasks import ping_single_host
from network_monitor.tasks.ping_tasks import ping_single_host
from network_monitor.tasks.schedule_tasks import ping_hosts
