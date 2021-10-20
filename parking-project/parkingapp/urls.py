from django.urls import path , include
from . import views
from allauth.account.views import confirm_email
from django.conf.urls import url
from django.contrib import admin


urlpatterns = [
    path('create/', views.CarCreate.as_view(), name='create-car'),
    path('', views.CarList.as_view()),
    path('<int:pk>/', views.CarDetail.as_view(), name='retrieve-car'),
    path('update/<int:pk>/', views.CarUpdate.as_view(), name='update-car'),
    path('delete/<int:pk>/', views.CarDelete.as_view(), name='delete-car'),
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),
    path('account/', include('allauth.urls')),
    url(r'^accounts-rest/registration/account-confirm-email/(?P<key>.+)/$', confirm_email, name='account_confirm_email'),
]