from django.urls import path
from . import views

urlpatterns = [
    path("ecowitt/", views.ecowitt_listener, name="ecowitt_listener"),
    path("", views.dashboard, name="dashboard"),  # Root → Dashboard
    path("dashboard/", views.dashboard, name="dashboard_alias"),  # optional Alias
    path("weather/<int:pk>/", views.weather_detail, name="weather_detail"),
]
