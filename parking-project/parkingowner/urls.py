from django.urls import path , include
from .views import ParkingOwnerCreate,ParkingOwnerDelete,ParkingOwnerDetail,ParkingOwnerUpdate,ParkingOwnerDelete,ParkingOwnerList,ParkingCreate


urlpatterns = [
    path('addparking/', ParkingCreate.as_view()),
    path('create/', ParkingOwnerCreate.as_view()),
    path('', ParkingOwnerList.as_view()),
    path('<int:pk>/', ParkingOwnerDetail.as_view()),
    path('update/', ParkingOwnerUpdate.as_view()),
    path('delete/<int:pk>/', ParkingOwnerDelete.as_view()),
]