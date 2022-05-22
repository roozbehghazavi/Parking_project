from django.urls import path , include
from .views import ParkingList, ReservationListParking, SupportDetail

urlpatterns = [
    path('parkinglist/', ParkingList.as_view()),
    path('reservelist/', ReservationListParking.as_view()),
    path('support_detail/', SupportDetail.as_view()),
]