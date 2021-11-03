from django.urls import path , include
from .views import ParkingCreate,ParkingDelete,ParkingList,ParkingDetail,ParkingOwnerDetail,ParkingOwnerUpdate,ParkingOwnerList


urlpatterns = [
    #Parking URLs
    path('createparking/', ParkingCreate.as_view()),
    path('parkinglist', ParkingList.as_view()),
    path('<int:pk>/', ParkingDetail.as_view()),
    path('deleteparking/', ParkingDelete.as_view()),
    

    #ParkingOwner URLs
    path('parkingownerlist', ParkingOwnerList.as_view()),
    path('<int:pk>/', ParkingOwnerDetail.as_view()),
    path('updateparkingowner/', ParkingOwnerUpdate.as_view())
]