from django.urls import path
from budget.views import DateSummary, DateDetail

urlpatterns = [
    path("datesummary/", DateSummary.DateSummaryView.as_view()),
    path("datedetail/", DateDetail.DateDetailView.as_view()),
]