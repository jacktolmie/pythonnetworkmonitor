import re
import subprocess
import sys

from ipaddress import ip_address
from xml.etree.ElementTree import tostring, Element

win = """Pinging google.ca [142.251.41.35] with 32 bytes of data:
Reply from 142.251.41.35: bytes=32 time=66ms TTL=119
Reply from 142.251.41.35: bytes=32 time=66ms TTL=119
Reply from 142.251.41.35: bytes=32 time=66ms TTL=119
Reply from 142.251.41.35: bytes=32 time=66ms TTL=119

Ping statistics for 142.251.41.35:
    Packets: Sent = 4, Received = 4, Lost = 30 (20% loss),
Approximate round trip times in milli-seconds:
    Minimum = 66ms, Maximum = 45ms, Average = 67ms"""

linux = """PING google.ca (142.251.41.35) 56(84) bytes of data.
64 bytes from yyz12s08-in-f3.1e100.net (142.251.41.35): icmp_seq=1 ttl=120 time=65.8 ms
64 bytes from yyz12s08-in-f3.1e100.net (142.251.41.35): icmp_seq=2 ttl=120 time=65.8 ms

--- google.ca ping statistics ---
2 packets transmitted, 2 received, 10% packet loss, time 1001ms
rtt min/avg/max/mdev = 65.776/65.787/65.799/0.011 ms
"""


# This function will check if for valid IP addresses and if num_pings is an int.
# Both IPv4 and IPv6 are checked.
def check_args(sent_address: str, num_pings: int) -> bool:
    try:
        ip_address(sent_address)
        if not isinstance(num_pings, int):
            return False
        return True
    except ValueError:
        return False


# This function will ping an address and return the results. If the
# node is not responding, it returns a message the ip not pingable
def ping_node(sent_address: str, num_pings: int = 5):
    # Check if arguments are valid.
    if not(check_args(sent_address, num_pings)):
        return "Invalid arguments"

    os = sys.platform
    print("Operating system:", os)
    try:
        # Check O/S. If windows, use -n, otherwise use -c for ping flag.
        return subprocess.check_output(
            ["ping", "-n" if os == "win32" else "-c", str(num_pings), sent_address]
        ).decode()

    except subprocess.CalledProcessError:
        return "Could not ping " + sent_address


# This function calls ping_node and checks the results. If not pingable
# return ping_node reply, otherwise return float of min/max/avg ping speeds;
def get_results(sent_address: str, num_pings: int = 5):
    # Check if arguments are valid.
    if not(check_args(sent_address, num_pings)):
        return "Invalid arguments"

    # Get ping response from ping_node.
    get_data = ping_node(sent_address, num_pings)

    # If IP not pingable, return get_data string
    if get_data.startswith("Could"):
        return get_data, False

    # os = sys.platform
    packets_lost, min_ping, max_ping, avg_ping = (None,) * 4

    op = "win32"  # reserve for testing windows
    # match op: # reserve for testing windows
    match sys.platform:
        # Match patterns for either Windows or Linux ping reply capture groups. Add them to the returned variables.
        case "linux" | "darwin" | "android":
            pattern = r"received, (\d+\.?\d*)[% a-zA-Z0-9\s\/=,]+mdev = (\d+.?\d+)\/(\d+.?\d+)\/(\d+.?\d+)"
            results = re.search(pattern, get_data)
            if results:
                packets_lost, min_ping, avg_ping, max_ping = results.groups()
                print(results)

        case "win32":
            pattern = r"Lost = \d+ \((\d+\.?\d*)[\s()0-9a-zA-Z%,-:=]+Minimum = (\d+)[a-zA-z, =]+(\d+)[a-zA-z, =]+(\d+)"
            results = re.search(pattern, win)
            if results:
                packets_lost, min_ping, max_ping, avg_ping = results.groups()
                print(results)

        case _:
            return "Invalid Operating System"

    # Return a list of floats, and one bool.
    return [float(x) for x in [packets_lost, min_ping, max_ping, avg_ping]], True
