
from modules import pingnode

test = pingnode.get_results("192.168.1.200", "2")
print(test)