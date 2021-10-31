from django.urls import path , include
from .views import ParkingAV,ParkingOwnerCreate,ParkingOwnerDelete,ParkingOwnerDetail,ParkingOwnerUpdate,ParkingOwnerDelete,ParkingOwnerList


urlpatterns = [
    path('addparking/', ParkingAV.as_view(), name='add-parking'),
    path('create/', ParkingOwnerCreate.as_view()),
    path('', ParkingOwnerList.as_view()),
    path('<int:pk>/', ParkingOwnerDetail.as_view()),
    path('update/<int:pk>/', ParkingOwnerUpdate.as_view()),
    path('delete/<int:pk>/', ParkingOwnerDelete.as_view()),
]