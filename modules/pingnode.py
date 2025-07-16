import re
import subprocess
import sys

# This function will ping an address and return the results. If the
# node is not responding, it returns a message the ip not pingable
def ping_node(sent_address: str, num_pings: int = 5):

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
def get_results(sent_address: str, hostname: str = "Node",  num_pings: int = 5):

    # Get ping response from ping_node.
    get_data = ping_node(sent_address, num_pings)

    # If IP not pingable, return get_data string
    if get_data.startswith("Could"):
        print(get_data)
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
