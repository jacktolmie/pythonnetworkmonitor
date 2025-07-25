# network_monitor/tasks/__init__.py

# Import specific tasks you want Celery to find directly
# Or, if you want Celery to discover all tasks within this package,
# you can leave this file empty, and rely on `autodiscover_tasks()`
# to traverse the package. However, explicit imports are generally clearer.

from .ping_tasks import ping_single_host # Import the specific task
from .schedule_tasks import ping_hosts   # Import the specific task