from django.urls import path , include

from .views import ManualEnterOrExit,ParkingDetail,ParkingCreate,ParkingDelete,ParkingList,ParkingDetail,ParkingOwnerDetail,ParkingOwnerUpdate,ParkingOwnerList,ParkingUpdate, PeriodsList,Validator


urlpatterns = [
    #Parking URLs
    path('createparking/', ParkingCreate.as_view()),
    path('updateparking/', ParkingUpdate.as_view()),
    path('parkinglist', ParkingList.as_view()),
    path('parkingdetail/', ParkingDetail.as_view()),
    path('deleteparking/', ParkingDelete.as_view()),
    

    #ParkingOwner URLs
    path('parkingownerlist', ParkingOwnerList.as_view()),
    path('<int:pk>/', ParkingOwnerDetail.as_view()),
    path('updateparkingowner/', ParkingOwnerUpdate.as_view()),

    #Validation URLs
    path('validation/',Validator.as_view()),


    #Shows all the periods of parking by id
    path('periodlist/', PeriodsList.as_view()),
    #manual exit or enter for parking operator
    path('manualexitorenter/', ManualEnterOrExit.as_view()),
]