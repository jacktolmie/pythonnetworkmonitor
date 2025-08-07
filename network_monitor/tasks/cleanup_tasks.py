# pythonnetworkmonitor/network_monitor/tasks/cleanup_tasks.py

import time

from celery import shared_task
from celery.utils.log import get_task_logger
from datetime import timedelta
from django.http import JsonResponse
from django.utils import timezone
from django.db import transaction

from network_monitor.models import PingHost, HostDowntimeEvent

logger = get_task_logger(__name__)

@shared_task(name="network_monitor.tasks.cleanup_tasks.delete_old_data")
def delete_old_data(host_id: int, delete_from_table: str, days_to_keep: int = 30):
    print(f"HOst ID: {host_id}")
    if not isinstance(host_id, int):
        host_id = int(host_id)

    if not isinstance(days_to_keep, int):
        days_to_keep = int(days_to_keep)

    logger.info(f"Starting cleanup task for Host ID: {host_id}. Deleting data older than {days_to_keep} days from table: {delete_from_table}...")

    # Calculate the cutoff date
    cutoff_date = timezone.now() - timedelta(days=days_to_keep)

    # Number of items to delete at a time in the database.
    batch_size = 1000

    # Delay time between deletions.
    delay_seconds = 0.1

    # Total number of rows deleted.
    total_deleted = 0

    try:
        if delete_from_table == "PingHost":
            while True:
                with transaction.atomic():
                    ping_ids_to_delete = list(
                        # This is the key change: Add the filter for host_id
                        PingHost.objects.filter(timestamp__lt=cutoff_date, host_id=host_id)
                        .order_by('id')
                        .values_list('id', flat=True)[:batch_size]
                    )

                    if not ping_ids_to_delete:
                        break

                    deleted_count, _ = PingHost.objects.filter(id__in=ping_ids_to_delete).delete()
                    total_deleted += deleted_count
                    logger.info(f"Deleted {deleted_count} PingHost records in current batch. Total deleted: {total_deleted}")

                if len(ping_ids_to_delete) < batch_size:
                    break

                time.sleep(delay_seconds)

            # These messages are moved outside the loop to be more accurate.
            print(f"Deleted {total_deleted} old PingHost records.")
            logger.info(f"Finished deleting old PingHost records. Total Pings deleted: {total_deleted}.")

        elif delete_from_table == "HostDowntimeEvent":

            while True:
                with transaction.atomic():
                    downtime_ids_to_delete = list(
                        # This is the key change: Add the filter for host_id
                        HostDowntimeEvent.objects.filter(start_time__lt=cutoff_date, host_id=host_id)
                        .order_by('id')
                        .values_list('id', flat=True)[:batch_size]
                    )

                    if not downtime_ids_to_delete:
                        break

                    deleted_count, _ = HostDowntimeEvent.objects.filter(id__in=downtime_ids_to_delete).delete()
                    total_deleted += deleted_count
                    logger.info(f"Deleted {deleted_count} HostDowntimeEvent records in current batch. Total deleted: {total_deleted}")

                if len(downtime_ids_to_delete) < batch_size:
                    break

                time.sleep(delay_seconds)

            # These messages are moved outside the loop to be more accurate.
            print(f"Deleted {total_deleted} old HostDowntimeEvent records.")
            logger.info(f"Finished deleting old HostDowntimeEvent records. Total Downtimes deleted: {total_deleted}.")

        else:
            print(f"No database table with the name {delete_from_table} exists or is supported.")
            logger.info(f"No database table with the name {delete_from_table} exists or is supported.")

        logger.info("Cleanup task completed successfully.")

        return JsonResponse({
            "total_deleted": total_deleted,
            'success': True,
        })

    except Exception as e:
        logger.error(f"Error during data cleanup task: {e}")
