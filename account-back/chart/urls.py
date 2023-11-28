from django.urls import path
from chart.views import date_summary,month_summary


urlpatterns = [
    path("datesummary/",date_summary.dateSummary.as_view()),
    path("monthsummary/",month_summary.monthSummary.as_view()),
]