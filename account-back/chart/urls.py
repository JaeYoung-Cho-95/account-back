from django.urls import path
from chart.views import date_summary


urlpatterns = [
    path("datesummary/",date_summary.dateSummary.as_view())
]