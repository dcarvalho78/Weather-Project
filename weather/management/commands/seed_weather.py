from django.core.management.base import BaseCommand
from weather.models import WeatherReading
import random

class Command(BaseCommand):
    help = "Seed database with dummy WeatherReading data"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.NOTICE("Seeding database with 50 WeatherReading entries..."))

        for _ in range(50):
            temp_c = round(random.uniform(-10, 35), 1)
            rain_mm = round(random.uniform(0, 10), 2)
            is_raining = rain_mm > 0

            WeatherReading.objects.create(
                stationtype="WS980WiFi",
                station_id="DEMO1234",
                temp_c=temp_c,
                humidity=random.randint(30, 100),
                wind_dir=random.randint(0, 360),
                wind_speed_mps=round(random.uniform(0, 15), 2),
                rain_mm=rain_mm,
                pressure_hpa=round(random.uniform(980, 1050), 1),
                uv=round(random.uniform(0, 11), 1),
                battery="OK",
                raw={"demo": True},
                is_raining=is_raining,
            )

        self.stdout.write(self.style.SUCCESS("Successfully seeded 50 WeatherReading entries."))
