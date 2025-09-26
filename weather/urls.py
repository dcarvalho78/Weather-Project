from django.urls import path
from . import views

urlpatterns = [
    path('ecowitt/', views.ecowitt_listener, name='ecowitt_listener'),
]
