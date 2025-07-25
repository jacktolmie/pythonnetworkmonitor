from django.db import models


# Host to be monitored.
class Host(models.Model):
    name =              models.CharField(max_length=255, unique=True,
                            help_text="A unique name for the host (e.g., 'Router_1', 'Web_Server')")
    ip_address =        models.GenericIPAddressField(unique=True, help_text="The IP address of the host.")
    description =       models.TextField(blank=True, null=True, help_text="Optional description of the host.")
    is_active =         models.BooleanField(default=True, help_text="Whether this host is currently being monitored.")
    added_date =        models.DateTimeField(auto_now_add=True, help_text="The date and time this host was added.")
    ping_interval =     models.IntegerField(null=True, default=60, blank=True, help_text="How many seconds between pings.")
    is_currently_down = models.BooleanField(default=False, help_text="True if the host is currently detected as down.")
    last_ping_time =    models.DateTimeField(null=True, blank=True, help_text="The last time this host was last ping.")

    def __str__(self):
        return f"{self.name} ({self.ip_address})"


# Results of the pings on the host.
class PingHost(models.Model):
    host =              models.ForeignKey(Host, on_delete=models.CASCADE, related_name='ping_results',
                             help_text="The host this ping result belongs to.")
    min_rtt =           models.FloatField(null=True, blank=True)
    max_rtt =           models.FloatField(null=True, blank=True)
    avg_rtt =           models.FloatField(null=True, blank=True)
    packet_loss =       models.IntegerField(null=True, blank=True)
    timestamp =         models.DateTimeField(auto_now_add=True)
    was_successful =    models.BooleanField(null=False, blank=True)

    def __str__(self):
        status = "UP" if self.was_successful else "DOWN"
        ping_val = f"{self.avg_rtt:.2f}ms" if self.avg_rtt is not None else "N/A"
        return f"{self.host.name} - {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')} - {status} ({ping_val})"

    class Meta:
        ordering = ["-timestamp"]


# If the host goes down, record time/date, and how long it is down.
class HostDowntimeEvent(models.Model):
    host =          models.ForeignKey(Host, on_delete=models.CASCADE, related_name='downtime_events',
                             help_text="The host that experienced downtime.")
    start_time =    models.DateTimeField(auto_now_add=True,
                                      help_text="The timestamp when the host was first detected as down.")
    end_time =      models.DateTimeField(null=True, blank=True,
                                    help_text="The timestamp when the host was detected as back up.")
    duration =      models.DurationField(null=True, blank=True,
                                    help_text="The duration of the downtime event (end_time - start_time).")
    reason =        models.CharField(max_length=255, null=True, blank=True,
                              help_text="Optional reason for downtime (e.g., 'network outage', 'server restart').")

    # confirmed_by =  models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.start_time and self.end_time and not self.duration:
            self.duration = self.end_time - self.start_time
        super().save(*args, **kwargs)

    def __str__(self):
        if self.end_time:
            return f"{self.host.name} Down from {self.start_time.strftime('%Y-%m-%d %H:%M')} to {self.end_time.strftime('%Y-%m-%d %H:%M')} ({self.duration})"
        return f"{self.host.name} Down since {self.start_time.strftime('%Y-%m-%d %H:%M')} (Ongoing)"

    class Meta:
        ordering = ['-start_time']  # Order downtime events by latest first
