import socket
from ipaddress import ip_address

# This function will check if for valid IP addresses and if num_pings is an int.
# Both IPv4, IPv6, and hostnames are checked.
def check_args(sent_address: str, num_pings: int) -> tuple[bool, str]:
    try:
        # Check if address is valid IPv4 or IPv6
        ip_address(sent_address)
        # Check if num_pings is an int.
        if not isinstance(num_pings, int):
            return False, sent_address
        return True, sent_address
    except ValueError:
        try:
            # Check if sent_address is a valid host name.
            check_address = socket.gethostbyaddr(sent_address)
            # print(check_address[2][0])
            # print("Valid IP address: %s" % sent_address)
            return True, check_address[2][0]

        except socket.gaierror as e:
            # print(e)
            return False, sent_address