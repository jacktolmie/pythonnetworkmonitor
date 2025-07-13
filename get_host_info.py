import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pythonnetworkmonitor.settings')
django.setup()

from modules import pingnode
from modules.save_data import save_data

def get_host_info(sent_host: str, save: bool, num_pings: int):
    # Strip off any whitespace.
    sent_host = sent_host.strip()

    # Check if the hostname or ip is valid.
    if pingnode.check_args(sent_host, 3):
        if save:
            ping_results, is_active = pingnode.get_results(sent_host, num_pings)
            print(ping_results)
            save_data(sent_host, ping_results, is_active)

        else :
            print(pingnode.ping_node(sent_host, num_pings))
    else :
        print("Invalid Hostname")
