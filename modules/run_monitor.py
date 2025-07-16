# pythonnetworkmonitor/management/commands/run_monitor.py
# (This is a Django management command, a good way to run background tasks)

import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from django.core.management.base import BaseCommand
from network_monitor.models import Host, PingHost

class Command(BaseCommand):
    help = 'Runs the network monitoring tasks in the background.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--interval',
            type=int,
            default=60,
            help='Interval in seconds between full monitoring runs (default: 60)',
        )
        parser.add_argument(
            '--workers',
            type=int,
            default=10, # Number of concurrent threads
            help='Number of concurrent worker threads for pinging (default: 10)',
        )
        parser.add_argument(
            '--duration',
            type=int,
            default=0, # 0 means run forever until stopped
            help='Duration in seconds to run the monitoring loop (0 for infinite)',
        )


    def handle(self, *args, **options):
        interval = options['interval']
        max_workers = options['workers']
        duration = options['duration']

        self.stdout.write(self.style.SUCCESS(f"Starting network monitor with {max_workers} worker threads, interval {interval}s."))
        if duration > 0:
            self.stdout.write(self.style.INFO(f"Monitoring will run for {duration} seconds."))

        start_time = time.time()

        while True:
            # Fetch active hosts from the database
            # You might want to filter by `is_active=True`
            hosts_to_monitor = Host.objects.filter(is_active=True)
            self.stdout.write(f"\nMonitoring {len(hosts_to_monitor)} hosts...")

            futures = []
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                for host in hosts_to_monitor:
                    # Submit the task to the thread pool
                    future = executor.submit(perform_and_save_ping, host.ip_address, host.name)
                    futures.append(future)

                # Wait for all submitted tasks to complete and process results
                for future in as_completed(futures):
                    try:
                        success = future.result() # Get the return value of perform_and_save_ping
                        # You can do something with 'success' here if needed
                    except Exception as exc:
                        self.stderr.write(self.style.ERROR(f'A task generated an exception: {exc}'))

            self.stdout.write(self.style.SUCCESS("All current ping tasks completed."))

            # Check if duration limit is reached
            if duration > 0 and (time.time() - start_time) >= duration:
                self.stdout.write(self.style.SUCCESS("Monitoring duration reached. Exiting."))
                break

            # Sleep until the next interval
            self.stdout.write(f"Sleeping for {interval} seconds before next run...")
            time.sleep(interval)