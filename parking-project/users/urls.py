from django.urls import path , include
from .views import CustomUserUpdate,UserInfo

urlpatterns = [
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),
    path('account/', include('allauth.urls')),
    path('update/', CustomUserUpdate.as_view()),
    path('userinfo/', UserInfo.as_view()),

    # url(r'^accounts-rest/registration/account-confirm-email/(?P<key>.+)/$', confirm_email, name='account_confirm_email'),
]