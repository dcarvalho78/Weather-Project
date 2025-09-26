from django.contrib import admin
from .models import WeatherReading

@admin.register(WeatherReading)
class WeatherReadingAdmin(admin.ModelAdmin):
    list_display = ('received_at','stationtype','station_id','temp_c','humidity','wind_speed_mps')
    readonly_fields = ('raw','received_at')
    ordering = ('-received_at',)
