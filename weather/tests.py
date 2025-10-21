from django.test import TestCase, Client
from django.urls import reverse
from .models import WeatherReading

class EcowittEndpointTest(TestCase):
    def test_post_saves_reading(self):
        c = Client()
        resp = c.post(reverse('ecowitt_listener'), {
            'stationtype': 'WS980WiFi',
            'tempf': '68.0',
            'humidity': '44'
        })
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(WeatherReading.objects.count(), 1)
        r = WeatherReading.objects.first()
        self.assertIsNotNone(r.temp_c)
        self.assertEqual(r.humidity, 44)
