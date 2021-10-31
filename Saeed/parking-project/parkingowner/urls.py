from django.urls import path , include
from .views import ParkingAV


urlpatterns = [
    path('addparking/', ParkingAV.as_view(), name='add-parking'),
]