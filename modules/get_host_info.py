import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pythonnetworkmonitor.settings')
django.setup()

from modules import pingnode, check_args
from modules.save_ping_results import save_ping_results

def get_host_info(hostname: str, host_ip: str, save: bool, num_pings: int):
    # Strip off any whitespace.
    hostname = hostname.strip()
    host_ip = host_ip.strip()

    # Check if the hostname or ip is valid.
    check_arguments = check_args.check_args(host_ip, num_pings)

    # Check if the check_arguments returned true. If so, check if the host_ip
    # matches the returned host_ip. If not, it was a hostname converted to an IP.
    if check_arguments[0]:
        if save:
            host_ip = host_ip if check_arguments[1] == host_ip else check_arguments[1]
            ping_results, is_active = pingnode.get_results(host_ip, hostname, num_pings)
            save_ping_results(hostname, host_ip, ping_results, is_active)

        else :
            # Need to find way to print this to web gui
            print(pingnode.ping_node(host_ip, num_pings))
    else :
        print("Invalid Hostname")
