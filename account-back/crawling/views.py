from rest_framework.views import APIView
from .task import save_money_news, save_economic_news
from background_task.models import Task
from rest_framework.response import Response
from rest_framework import status
from crawling.utility import economic_review, money_today
from logging import getLogger
logger = getLogger("A")

# Create your views here.
class ReservationCheck(APIView):
    def get(self, request):
        # repeat=Task.DAILY
        # save_economic_news()
        # save_money_news()
        eco_crawling = economic_review.EconomicCrawling(
            news="eco",
            homepage="https://www.econovill.com/",
            crawling_url="https://www.econovill.com/news/articleList.html?sc_section_code=S1N32&view_type=sm",
        )
        eco_crawling.save()
        
        money_crawling = money_today.MoneyCrawling(
            news="money",
            homepage="",
            crawling_url="https://news.mt.co.kr/newsList.html?pDepth1=bank&pDepth2=Btotal",
        )
        logger.info("4")
        money_crawling.save()
        logger.info("5")
        return Response(status=status.HTTP_302_FOUND)