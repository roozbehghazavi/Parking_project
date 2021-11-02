from django.urls import path , include
from .views import addParking,ParkingOwnerCreate,ParkingOwnerDelete,ParkingOwnerDetail,ParkingOwnerUpdate,ParkingOwnerDelete,ParkingOwnerList,ParkingCreate


urlpatterns = [
    path('addparking/', addParking.as_view(), name='add-parking'),
    path('create/', ParkingOwnerCreate.as_view()),
    path('', ParkingOwnerList.as_view()),
    path('<int:pk>/', ParkingOwnerDetail.as_view()),
    path('update/', ParkingOwnerUpdate.as_view()),
    path('delete/<int:pk>/', ParkingOwnerDelete.as_view()),
]