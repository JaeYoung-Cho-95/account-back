from rest_framework.views import APIView
from .task import save_money_news, save_economic_news
from background_task.models import Task
from rest_framework.response import Response
from rest_framework import status
from crawling.utility import economic_review, money_today
from crawling.models import NewsModel
from crawling.serializers import NewsSerializer
from rest_framework.pagination import PageNumberPagination
import os

# Create your views here.
class ReservationCheck(APIView):
    def get(self, request):
        save_economic_news()
        save_money_news()
        
        os.system("aws s3 sync /usr/src/account-back/images s3://accountbookbucket/images")
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
            for idx in range(len(serializer.data)):
                if not serializer.data[idx]["img_url"]:
                    continue
                serializer.data[idx]["img_url"] = serializer.data[idx]["img_url"][21:]
            return Response(serializer.data)
        
        serializer = NewsSerializer(queryset, many=True)
        return Response(serializer.data)