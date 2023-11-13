from django.urls import path
from budget.views import MonthSummary

urlpatterns = [
    path("monthsummary/", MonthSummary.MonthSummaryView.as_view())
]