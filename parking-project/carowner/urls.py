from django.urls import path , include

from carowner.views import CarCreate, CarDelete, CarList, CarOwnerCreate, CarOwnerDetail, CarOwnerUpdate, CarOwnerDelete, CarOwnerList, ParkingList


urlpatterns = [
    path('create/', CarOwnerCreate.as_view()),
    path('', CarOwnerList.as_view()),
    path('<int:pk>/', CarOwnerDetail.as_view()),
    path('update/', CarOwnerUpdate.as_view()),
    path('delete/<int:pk>/', CarOwnerDelete.as_view()),
    ###Car Views Functions
    path('carcreate/', CarCreate.as_view()),
    path('carlist/',CarList.as_view()),
    path('cardelete/', CarDelete.as_view()),
    ###Parking List
    path('parkinglist/',ParkingList.as_view()),
]