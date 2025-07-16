from modules import get_host_info

server = "192.168.1.200"
hostname = "Test1"
server1 = "192.168.1.203"
hostname1 = "Test2"
server2 = "bork-and-borr"
hostname2 = "Bork-and-borr"
server3 = "asdf"
hostname3 = "asdf"

get_host_info.get_host_info(hostname, server, True, 2)
get_host_info.get_host_info(hostname1, server1, True, 2)
get_host_info.get_host_info(hostname2, server2, True, 2)
get_host_info.get_host_info(hostname3, server3, True, 2)

# ip6 = "2001:0db8:0001:0000:0000:0ab9:C0A8:0102"
# get_host_info.get_host_info(ip6, True, 2)