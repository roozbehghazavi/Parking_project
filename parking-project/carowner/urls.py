from django.urls import path , include
from carowner.views import AddCredit, AddRate, CarCreate, CarDelete, CarList, CarUpdate, CarOwnerCreate, CarOwnerDetail, \
    CarOwnerUpdate, CarOwnerDelete, CarOwnerList, CommentChildCreate, CommentDelete, CommentList, CommentParentCreate, \
    CommentUpdate, IsRated, ParkingList, ParkingSearch, PassedReservationListCarOwner, ReservationCreate, \
    ReservationListCarOwner, ReservationDelete, ReservationWithoutEndtime, GetMinMaxPrice, RecentParkings, \
    MostPopularParkings, AddParkingMonitor

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
    #Add credit to carowner
    path('add-credit/', AddCredit.as_view()),

    


    ###Car Urls


    #create a car
    path('carcreate/', CarCreate.as_view()),
    #list of all cars owned by the logged in CarOwner
    path('carlist/',CarList.as_view()),
    #delete a car by id
    path('cardelete/', CarDelete.as_view()),
    #edit a car by id
    path('carupdate/', CarUpdate.as_view()),


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
    path('commentlist/',CommentList.as_view()),


    ###Rating Urls


    #Add rating to a parking
    path('addrate/', AddRate.as_view()),
    #Show if the user rated or not
    path('israted/', IsRated.as_view()),

    ###Reservation

    #reserve a parking
    path('reserve/', ReservationCreate.as_view()),
    #Delete a reservation
    path('delete_reserve/', ReservationDelete.as_view()),
    #reserve without endtime
    path('reserve_without_endtime/', ReservationWithoutEndtime.as_view()),
    #reserve list for carowner
    path('reservelist/', ReservationListCarOwner.as_view()),
    #passed reserve list for carowner
    path('passedreservelist/', PassedReservationListCarOwner.as_view()),


    ###Search parking
    path('parkingsearch/', ParkingSearch.as_view(), name='parking_search'),
    path('get_min_max_price/', GetMinMaxPrice.as_view(), name='get_min_max_price'),
    path('get_recent_parkings/', RecentParkings.as_view(), name='get_recent_parkings'),
    path('get_most_popular_parkings/', MostPopularParkings.as_view(), name='get_most_popular_parkings'),
    path('search_click/', AddParkingMonitor.as_view(), name='search_click'),
]