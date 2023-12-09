from rest_framework.views import APIView
from .task import save_money_news, save_economic_news
from background_task.models import Task
from rest_framework.response import Response
from rest_framework import status
from crawling.utility import economic_review, money_today
from crawling.models import NewsModel
from crawling.serializers import NewsSerializer
from logging import getLogger
from rest_framework.pagination import PageNumberPagination


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
        money_crawling.save()
        return Response(status=status.HTTP_302_FOUND)

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000
    
class NewsAPI(APIView):
    pagination_class = StandardResultsSetPagination
    
    def get(self, request):
        queryset = NewsModel.objects.all().order_by("-id")
        page = self.pagination_class().paginate_queryset(queryset, request)
        
        if page:
            serializer = NewsSerializer(page, many=True)
            return Response(serializer.data)
        
        serializer = NewsSerializer(queryset, many=True)
        return Response(serializer.data)