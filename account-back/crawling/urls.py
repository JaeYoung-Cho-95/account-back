from django.urls import path
from crawling.views import ReservationCheck

urlpatterns = [
    path('states/', ReservationCheck.as_view())   
]