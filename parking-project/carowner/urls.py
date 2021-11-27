from django.urls import path , include
from carowner.views import AddRate, CarCreate, CarDelete, CarList, CarOwnerCreate, CarOwnerDetail, CarOwnerUpdate, CarOwnerDelete, CarOwnerList,CommentChildCreate, CommentDelete, CommentList, CommentParentCreate, CommentUpdate, IsRated, ParkingList, ReservationCreate


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


    ###Comment Urls

    #Add a comment
    path('addcomment/',CommentParentCreate.as_view()),
    #edit a comment
    path('editcomment/',CommentUpdate.as_view()),
    #delete a comment
    path('deletecomment/',CommentDelete.as_view()),
    #Add a reply to a comment
    path('addreply/',CommentChildCreate.as_view()),
    #list of all parking's comments
    path('commentlist/<int:id>/',CommentList.as_view()),


    ###Rating Urls


    #Add rating to a parking
    path('addrate/', AddRate.as_view()),
    #Show if the user rated or not
    path('israted/<int:id>/', IsRated.as_view()),

    path('reserve/', ReservationCreate.as_view()),


]