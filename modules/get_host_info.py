import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pythonnetworkmonitor.settings')
django.setup()

from modules import pingnode, check_args
from modules.save_ping_results import save_ping_results

def get_host_info(hostname: str, host_ip: str, save: bool, num_pings: int = 5) -> tuple[str, str]:
    # Strip off any whitespace.
    hostname =  hostname.strip()
    host_ip =   host_ip.strip()

    # Check if the hostname or ip is valid.
    check_arguments = check_args.check_args(host_ip, num_pings)

    # Check if the check_arguments returned true. If so, check if the host_ip
    # matches the returned host_ip. If not, it was a hostname converted to an IP.
    if check_arguments[0]:
        if save:
            # Checks if the returned IP was the host_ip, or address from host name ping.
            host_ip = host_ip if check_arguments[1] == host_ip else check_arguments[1]

            # Get results of pinging host.
            ping_results, is_active = pingnode.get_results(host_ip, hostname, num_pings)

            # Add host to database.
            add_result = save_ping_results(hostname, host_ip, ping_results, is_active)

            test = add_result[0]
            return ("success", add_result[1]) if add_result[0] else ("failure", add_result[1])

        else :
            # Return the ping results, and a blank string since it is a tuple being returned.
            return pingnode.ping_node(host_ip, num_pings), ""
    else :
        return f"Invalid Hostname {hostname}", "Please enter a valid Hostname"
