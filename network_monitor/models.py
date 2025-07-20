from django.db import models

# Host to be monitored.
class Host(models.Model):

    name = models.CharField(max_length=255, unique=True, help_text="A unique name for the host (e.g., 'Router_1', 'Web_Server')")
    ip_address =    models.GenericIPAddressField(unique=True, help_text="The IP address of the host.")
    description =   models.TextField(blank=True, null=True, help_text="Optional description of the host.")
    is_active =     models.BooleanField(default=True, help_text="Whether this host is currently being monitored.")
    added_date =    models.DateTimeField(auto_now_add=True, help_text="The date and time this host was added.")
    ping_interval = models.IntegerField(null=True, blank=True, default=1)

    def __str__(self):
        return f"{self.name} ({self.ip_address})"

# Results of the pings on the host.
class PingHost(models.Model):
    host =          models.ForeignKey(Host, on_delete=models.CASCADE, related_name='ping_results', help_text="The host this ping result belongs to.")
    min_rtt =       models.FloatField(null=True, blank=True)
    max_rtt =       models.FloatField(null=True, blank=True)
    avg_rtt =       models.FloatField(null=True, blank=True)
    packet_loss =   models.IntegerField(null=True, blank=True)
    timestamp =     models.DateTimeField(auto_now_add=True)
    was_successful =models.BooleanField(null=False, blank=True)
    last_downtime = models.DateTimeField(null=True, blank=True)


    def __str__(self):
        status =    "UP" if self.was_successful else "DOWN"
        ping_val =  f"{self.avg_rtt:.2f}ms" if self.avg_rtt is not None else "N/A"
        return f"{self.host.name} - {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')} - {status} ({ping_val})"


class Meta:
        ordering = ["-timestamp"]