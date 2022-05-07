from django.urls import path , include
from .views import ParkingList

urlpatterns = [
    path('parkinglist/', ParkingList.as_view()),
]