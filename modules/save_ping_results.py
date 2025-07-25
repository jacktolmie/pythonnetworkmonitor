from django.db import transaction, IntegrityError, OperationalError

from django.utils import timezone
from network_monitor.models import Host, PingHost, HostDowntimeEvent


# This function creates or checks for existing host in the database, and saves ping results.
def save_ping_results(hostname: str, host_ip: str, data: list[int], was_successful: bool) -> tuple[bool, str]:

    try:
        with (transaction.atomic()):
            # Check if host exists already, or creates a new one in the database Host table.
            host_object, created = Host.objects.get_or_create(name=hostname, defaults={'ip_address':host_ip})

            # Check if the IP address changed if the host exists.
            if not created and host_object.ip_address != host_ip:
                host_object.ip_address = host_ip
                host_object.save()

            # Adds results to the database PingHost table.
            ping_result = PingHost.objects.create(host=host_object, was_successful=was_successful)
            ping_result.was_successful = was_successful
            ping_result.timestamp = timezone.now()

            if was_successful:
                ping_result.packet_loss =   data[0]
                ping_result.min_rtt =       data[1]
                ping_result.max_rtt =       data[2]
                ping_result.avg_rtt =       data[3]
                host_object.last_ping_time = timezone.now()

                if host_object.is_currently_down:
                    host_object.is_currently_down = False
                    host_object.last_ping_time =    timezone.now()
                    get_host_downtime =             HostDowntimeEvent.objects.\
                            filter(host=host_object, end_time__isnull=True).reverse()
                    if get_host_downtime.exists():
                        for hosts in get_host_downtime:
                            hosts.end_time = timezone.now()
                            hosts.save()

            else:
                if not host_object.is_currently_down:
                    ping_result.last_downtime =     timezone.now()
                    host_object.is_currently_down = True
                    HostDowntimeEvent.objects.create(host=host_object, start_time=timezone.now()).save()

            # Save the results to the database.
            ping_result.save()
            host_object.save()


            return (True, f"{hostname} with ip {host_ip} was created successfully") if created \
                else (False,f"{hostname} with ip {host_ip} was already being monitored")

    except IntegrityError as e:
        return False, f"Database Integrity Error for {host_ip}: {e}"

    except OperationalError as e:
        return False, f"Database Operational Error for {host_ip}: Could not connect or issue with DB: {e}"

    except Exception as e:
        return False, f"An unexpected error occurred while saving for {host_ip}: {e}"
