from django.urls import path , include

from carowner.views import CarCreate, CarDelete, CarList, CarOwnerCreate, CarOwnerDetail, CarOwnerUpdate, CarOwnerDelete, CarOwnerList, ParkingList


urlpatterns = [
    ###CarOwner Urls

    path('create/', CarOwnerCreate.as_view()),
    path('list/', CarOwnerList.as_view()),
    #return logged in CarOwner
    path('detail/', CarOwnerDetail.as_view()),
    #update logged in CarOwner
    path('update/', CarOwnerUpdate.as_view()),
    #Delete logged in CarOwner
    path('delete/', CarOwnerDelete.as_view()),

    ###Car Urls

    #create a car
    path('carcreate/', CarCreate.as_view()),
    #list of all cars owned by the logged in CarOwner
    path('carlist/',CarList.as_view()),
    #delete a car by id
    path('cardelete/', CarDelete.as_view()),

    ###Parking Urls

    #list of all parkings
    path('parkinglist/',ParkingList.as_view()),
]