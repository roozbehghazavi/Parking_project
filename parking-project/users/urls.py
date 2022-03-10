from django.urls import path , include
from .views import CustomUserUpdate,UserRole,CustomLoginView,FacebookLogin,GoogleLogin

urlpatterns = [
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),
    path('account/', include('allauth.urls')),
    path('update/', CustomUserUpdate.as_view()),
    path('userrole/', UserRole.as_view()),
    path('custom/login/', CustomLoginView.as_view()),
    path('rest-auth/facebook/', FacebookLogin.as_view(), name='fb_login'),
    path('rest-auth/google/', GoogleLogin.as_view(), name='google_login'),
]