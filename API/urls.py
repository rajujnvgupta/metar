from django.urls import path
from . import views

urlpatterns = [
    path("info", views.weather_status, name="weather_status"),
    path("redis_details", views.redis_details, name='redis_details'),
    path("ping", views.ping, name="ping"),
    path("status_check", views.status, name="status_check"),
]