from django.urls import path , include
from .views import CustomUserUpdate,UserRole,CustomLoginView

urlpatterns = [
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', include('rest_auth.registration.urls'), name="register"),
    path('account/', include('allauth.urls')),
    path('update/', CustomUserUpdate.as_view(), name='edit-profile'),
    path('userrole/', UserRole.as_view()),
    path('custom/login/', CustomLoginView.as_view()),

    # url(r'^accounts-rest/registration/account-confirm-email/(?P<key>.+)/$', confirm_email, name='account_confirm_email'),
]