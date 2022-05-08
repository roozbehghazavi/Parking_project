from django.urls import path , include
from .views import ParkingList,ReservationListParking

urlpatterns = [
    path('parkinglist/', ParkingList.as_view()),
    path('reservelist/', ReservationListParking.as_view()),
]