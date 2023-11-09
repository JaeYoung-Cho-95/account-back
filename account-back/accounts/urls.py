from django.urls import path
from accounts.views import UserLogin, UserCreate, UserDetail, CustomTokenRefresh, UserLogout
from rest_framework_simplejwt.views import TokenVerifyView


urlpatterns = [
    path("signup/", UserCreate.UserCreateView.as_view()),
    path("login/", UserLogin.UserLoginView.as_view()),
    path("logout/", UserLogout.userLogOutView.as_view()),
    path("login/verify/", TokenVerifyView.as_view()),
    path("login/refresh/", CustomTokenRefresh.CustomTokenRefreshView.as_view()),
    path("detail/", UserDetail.UserDetailView.as_view()),
]
