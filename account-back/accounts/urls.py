from django.urls import path, include
from .views import UserLogin, UserCreate
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)


urlpatterns = [
    path("signup/", UserCreate.UserCreateView.as_view()),
    path("login/", UserLogin.UserLoginView.as_view(), name="login_with_token"),
    path("login/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("login/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]