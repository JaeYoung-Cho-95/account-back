from django.urls import path
from chart.views import date_summary, month_summary, tag_top10


urlpatterns = [
    path("datesummary/", date_summary.dateSummary.as_view()),
    path("monthsummary/", month_summary.monthSummary.as_view()),
    path("tagtopten/", tag_top10.TagTopTenView.as_view())
]
