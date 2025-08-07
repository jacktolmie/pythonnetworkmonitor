from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from datetime import timedelta
import random

# Import your models
# Assuming Ping and Downtime models exist in network_monitor/models.py
from network_monitor.models import PingHost, HostDowntimeEvent, Host


class Command(BaseCommand):
    help = 'Generates a specified number of old Ping and Downtime records for testing cleanup.'

    def add_arguments(self, parser):
        """
        Adds command-line arguments for the management command.
        """
        parser.add_argument(
            '--num_records',
            type=int,
            default=10000,  # Default number of records to generate
            help='Number of old records to generate for each model (Ping and Downtime).'
        )
        parser.add_argument(
            '--days_old_max',
            type=int,
            default=60,  # Max days old for generated data
            help='Maximum number of days old for the generated data. Records will be randomly set between 1 and this value.'
        )
        parser.add_argument(
            '--host_id',
            type=int,
            default=1,  # Default host ID to associate with generated data
            help='The ID of the Host to associate with the generated Ping/Downtime records.'
        )

    def handle(self, *args, **options):
        """
        The main logic for the management command.
        """
        num_records = 5000 #options['num_records']
        days_old_max = 90 #options['days_old_max']
        host_id = 1 #options['host_id']

        self.stdout.write(self.style.SUCCESS(
            f"Generating {num_records} old Ping and Downtime records "
            f"for Host ID {host_id}, up to {days_old_max} days old..."
        ))

        try:
            # Verify the host exists
            try:
                host_instance = Host.objects.get(pk=host_id)
            except Host.DoesNotExist:
                raise CommandError(f"Host with ID {host_id} does not exist. Please create it first.")

            current_time_for_generation = timezone.now()
            # Generate Ping records
            ping_records = []
            for i in range(num_records):
                # Randomly set timestamp between 1 day and days_old_max
                days_ago = random.randint(1, days_old_max)
                hours_ago = random.randint(0, 23)
                minutes_ago = random.randint(0, 59)

                # Calculate old_timestamp relative to the fixed current_time_for_generation
                old_timestamp = current_time_for_generation - timedelta(
                    days=days_ago,
                    hours=hours_ago,
                    minutes=minutes_ago
                )
                ping_records.append(
                    PingHost(
                        host=host_instance,
                        timestamp=old_timestamp,
                        min_rtt=random.uniform(5, 20),
                        avg_rtt=random.uniform(20, 50),
                        max_rtt=random.uniform(50, 100),
                        packet_loss=random.uniform(0, 10),
                        was_successful=True
                        # status_code=200  # Assuming 200 for successful pings
                    )
                )
                # Print progress every 1000 records
                if (i + 1) % 1000 == 0:
                    self.stdout.write(f"Generated {i + 1} Ping records...")

            # Bulk create for efficiency
            PingHost.objects.bulk_create(ping_records)
            self.stdout.write(self.style.SUCCESS(f"Successfully created {len(ping_records)} old Ping records."))

            # Generate Downtime records (optional, if you have this model)
            downtime_records = []
            for i in range(num_records // 10):  # Generate fewer downtime records, as they are less frequent
                days_ago = random.randint(1, days_old_max)
                old_timestamp = timezone.now() - timedelta(days=days_ago, hours=random.randint(0, 23),
                                                           minutes=random.randint(0, 59))

                # Ensure start_time is before end_time for downtime
                start_time = old_timestamp
                end_time = start_time + timedelta(minutes=random.randint(1, 60))  # Random downtime duration

                downtime_records.append(
                    HostDowntimeEvent(
                        host=host_instance,
                        start_time=start_time,
                        end_time=end_time,
                        reason=random.choice(["Network outage", "Server reboot", "Maintenance", "Unknown"])
                    )
                )
                if (i + 1) % 1000 == 0:
                    self.stdout.write(f"Generated {i + 1} Downtime records...")

            if downtime_records:
                HostDowntimeEvent.objects.bulk_create(downtime_records)
                self.stdout.write(
                    self.style.SUCCESS(f"Successfully created {len(downtime_records)} old Downtime records."))
            else:
                self.stdout.write(
                    self.style.WARNING("No Downtime records generated (model might not exist or num_records too low)."))

            self.stdout.write(self.style.SUCCESS("Old data generation complete!"))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"An error occurred during data generation: {e}"))
            raise CommandError(f"Data generation failed: {e}")

