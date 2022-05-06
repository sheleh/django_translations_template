from django.urls import path
from app.api.views import (
    UserCreateApiView,
    UserAuthenticationAPIView,
    UserChangePasswordAPIView,
    UserSwitchLanguageAPIView,
    UserLogoutAPIView,
)


urlpatterns = [
    path('users/login/', UserAuthenticationAPIView.as_view(), name='user_login'),
    path('users/logout/', UserLogoutAPIView.as_view(), name='user_logout'),
    path('users/register/', UserCreateApiView.as_view(), name='user_create'),
    path('users/change-password/', UserChangePasswordAPIView.as_view(), name='user_change_password'),
    path('users/switch-lang/', UserSwitchLanguageAPIView.as_view(), name='user_switch_lang'),
]
