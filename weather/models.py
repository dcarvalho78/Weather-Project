from django.db import models
from django.utils import timezone

try:
    from django.db.models import JSONField as BuiltinJSONField
except Exception:
    BuiltinJSONField = None

JSON_FIELD = BuiltinJSONField if BuiltinJSONField is not None else models.JSONField

class WeatherReading(models.Model):
    received_at = models.DateTimeField(default=timezone.now, db_index=True)
    stationtype = models.CharField(max_length=100, blank=True, null=True)
    station_id = models.CharField(max_length=100, blank=True, null=True)
    temp_c = models.FloatField(blank=True, null=True)
    humidity = models.IntegerField(blank=True, null=True)
    wind_dir = models.IntegerField(blank=True, null=True)
    wind_speed_mps = models.FloatField(blank=True, null=True)
    rain_mm = models.FloatField(blank=True, null=True)
    pressure_hpa = models.FloatField(blank=True, null=True)
    uv = models.FloatField(blank=True, null=True)
    battery = models.CharField(max_length=50, blank=True, null=True)
    raw = JSON_FIELD(blank=True, null=True)

    class Meta:
        ordering = ("-received_at",)

    def __str__(self):
        return f"{self.stationtype or 'station'} @ {self.received_at.isoformat()}"
