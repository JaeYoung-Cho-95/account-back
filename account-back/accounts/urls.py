from django.urls import path
from accounts.views import UserLogin, UserCreate, UserDetail, CustomTokenRefresh
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)


urlpatterns = [
    path("signup/", UserCreate.UserCreateView.as_view()),
    path("login/", UserLogin.UserLoginView.as_view(), name="login_with_token"),
    path("login/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("login/refresh/", CustomTokenRefresh.CustomTokenRefreshView.as_view(), name="token_refresh"),
    path("detail/", UserDetail.UserDetailView.as_view()),
]
