import subprocess
import sys
import re

win = """Pinging google.ca [142.251.41.35] with 32 bytes of data:
Reply from 142.251.41.35: bytes=32 time=66ms TTL=119
Reply from 142.251.41.35: bytes=32 time=66ms TTL=119
Reply from 142.251.41.35: bytes=32 time=66ms TTL=119
Reply from 142.251.41.35: bytes=32 time=66ms TTL=119

Ping statistics for 142.251.41.35:
    Packets: Sent = 4, Received = 4, Lost = 0 (0% loss),
Approximate round trip times in milli-seconds:
    Minimum = 66ms, Maximum = 45ms, Average = 67ms"""

linux = """PING 192.168.1.200 (192.168.1.200) 56(84) bytes of data.
64 bytes from 192.168.1.200: icmp_seq=1 ttl=64 time=0.495 ms
64 bytes from 192.168.1.200: icmp_seq=2 ttl=64 time=0.467 ms
64 bytes from 192.168.1.200: icmp_seq=3 ttl=64 time=0.409 ms

--- 192.168.1.200 ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2056ms
rtt min/avg/max/mdev = 0.409/0.457/0.495/0.035 ms
"""

# This function will ping an address and return the results. If the
# node is not responding, it returns a message the ip not pingable
def ping_node(ip_address, num_pings = "5"):

    os = sys.platform
    print("Operating system:", os)
    try:
        # Check O/S. If windows, user -n, otherwise use -c for ping flag.
        return subprocess.check_output(["ping", "-n" if os == "win32" else "-c", num_pings, ip_address]).decode()

    except subprocess.CalledProcessError:
       return "Could not ping " + ip_address


def get_breakdown(ip_address, num_pings = "5"):
    # Get ping response from ping_node.
    get_data = ping_node(ip_address, num_pings)

    # If IP not pingable, return get_data string
    if get_data.startswith("Could"):
        return get_data

    # os = sys.platform
    min_ping, max_ping, avg_ping = (None,)*3

    op = "win32" # reserve for testing windows

    match sys.platform:
        case "linux" | "darwin" | "android":
            pattern = r"(\d+\.\d+)/(\d+\.\d+)/(\d+\.\d+)"
            results = re.search(pattern, get_data)
            if results:
                 min_ping, avg_ping, max_ping = results.groups()

        case "win32":
            pattern = r"Minimum = (\d+)[a-zA-z, =]+(\d+)[a-zA-z, =]+(\d+)"
            results = re.search(pattern, win)
            if results:
                min_ping, max_ping, avg_ping = results.groups()

        case _:
            return "Invalid Operating System"

    return [float(x) for x in [min_ping, max_ping, avg_ping]]