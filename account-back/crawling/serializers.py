from rest_framework.serializers import ModelSerializer
from crawling.models import NewsModel


class NewsSerializer(ModelSerializer):
    class Meta:
        model = NewsModel
        fields = ["title", "content", "img_url", "news_url"]
