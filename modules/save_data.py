import datetime

from network_monitor.models import PingHost

# def save_data(host: str, data: list[int]):
def save_data(host: str, data: list[int], is_active: bool):
    get_data =                  PingHost()
    get_data.host =             host
    get_data.timestamp =        datetime.datetime.now()
    get_data.packet_loss =      data[0]
    get_data.is_active =        is_active
    if is_active:
        get_data.min_rtt =     data[1]
        get_data.max_rtt =     data[2]
        get_data.avg_rtt =     data[3]

    get_data.save()

