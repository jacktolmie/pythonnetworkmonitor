from django.db import models

class PingHost(models.Model):
    host =          models.CharField(max_length=200)
    min_rtt =       models.FloatField(null=True, blank=True)
    max_rtt =       models.FloatField(null=True, blank=True)
    avg_rtt =       models.FloatField(null=True, blank=True)
    packet_loss =   models.IntegerField(null=True, blank=True)
    timestamp =     models.DateTimeField(auto_now_add=True)
    is_active =     models.BooleanField(null=False, blank=True)

    def __str__(self):
        return f"Ping to {self.host} at {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"

    class Meta:
        ordering = ["-timestamp"]