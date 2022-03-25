from django.urls import path , include
<<<<<<< HEAD
from .views import CustomUserUpdate,UserRole,CustomLoginView,GoogleLogin,FacebookLogin
=======
from .views import CustomUserUpdate,UserRole,CustomLoginView,FacebookLogin,GoogleLogin
>>>>>>> 82b17d1397420d321a2c647db8e88fb219b7ba9b

urlpatterns = [
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', include('rest_auth.registration.urls'), name="register"),
    path('rest-auth/facebook/', FacebookLogin.as_view(), name='fb_login'),
    path('rest-auth/google/', GoogleLogin.as_view(), name='google_login'),
    path('account/', include('allauth.urls')),
    path('update/', CustomUserUpdate.as_view(), name='edit-profile'),
    path('userrole/', UserRole.as_view()),
    path('custom/login/', CustomLoginView.as_view()),
<<<<<<< HEAD
=======
    path('rest-auth/facebook/', FacebookLogin.as_view(), name='fb_login'),
    path('rest-auth/google/', GoogleLogin.as_view(), name='google_login'),

    # url(r'^accounts-rest/registration/account-confirm-email/(?P<key>.+)/$', confirm_email, name='account_confirm_email'),
>>>>>>> 82b17d1397420d321a2c647db8e88fb219b7ba9b
]