from django.urls import path , include

from .views import CurrentPeriod, EditParkingTemplate, OverallCustomers, PassedReservationListParking, ReservationListParking,ManualEnterOrExit,ParkingDetail,ParkingCreate,ParkingDelete,ParkingList,ParkingDetail,ParkingOwnerDetail,ParkingOwnerUpdate,ParkingOwnerList,ParkingUpdate, PeriodsList, TemplateDetail,Validator,OverallIncome
OverallCustomers,

urlpatterns = [
    #Parking URLs
    path('createparking/', ParkingCreate.as_view(), name='add_parking'),
    path('updateparking/', ParkingUpdate.as_view()),
    path('parkinglist/', ParkingList.as_view()),
    path('parkingdetail/', ParkingDetail.as_view()),
    path('deleteparking/', ParkingDelete.as_view()),
    #parking template url
    path('edittemplate/', EditParkingTemplate.as_view()),
    #gets template of a parking
	path('templatedetail/', TemplateDetail.as_view()),
    

    #ParkingOwner URLs
    path('parkingownerlist/', ParkingOwnerList.as_view()),
    path('<int:pk>/', ParkingOwnerDetail.as_view()),
    path('updateparkingowner/', ParkingOwnerUpdate.as_view()),

    #Validation URLs
    path('validation/',Validator.as_view()),

    #Shows all the periods of parking by id
    path('periodlist/', PeriodsList.as_view()),
    #Shows current period
    path('currentperiod/', CurrentPeriod.as_view()),
    #manual exit or enter for parking operator
    path('manualexitorenter/', ManualEnterOrExit.as_view()),
    #Reservation list for parking owner
    path('reservelist/', ReservationListParking.as_view()),
    #Passed reservation list for parking owner
    path('passedreservelist/', PassedReservationListParking.as_view()),
    #Overall income by date
    path('income/', OverallIncome.as_view()),
    path('allcustomers/',OverallCustomers.as_view()),
    # path('combinedlist/',CombinedList.as_view()),

]