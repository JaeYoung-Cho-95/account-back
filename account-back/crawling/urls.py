from django.urls import path
from crawling.views import ReservationCheck, NewsAPI

urlpatterns = [
    path("states/", ReservationCheck.as_view()),
    path("list/", NewsAPI.as_view()),
]
