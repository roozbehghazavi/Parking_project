# chat/urls.py
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('rooms/users/', views.rooms, name='rooms'),
    path('<str:room_name>/', views.room, name='room'),
]