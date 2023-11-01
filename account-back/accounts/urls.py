from django.urls import path, include
from .views import UserCreateView

urlpatterns = [
    # path('', include('dj_rest_auth.urls')),
    path('signup/', UserCreateView.as_view()),
]