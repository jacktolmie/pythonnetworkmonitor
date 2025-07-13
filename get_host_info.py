import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pythonnetworkmonitor.settings')
django.setup()

from modules import pingnode
from modules.save_data import save_data

def get_host_info(sent_host: str):
    ping_results, is_active = pingnode.get_results(sent_host, 2)
    save_data(sent_host, ping_results, is_active)
