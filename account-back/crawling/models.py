from django.db import models

# Create your models here.
class NewsModel(models.Model):
    title = models.TextField(blank=False)
    content = models.TextField(blank=False)
    img_url = models.TextField(default=None, null=True)
    news_url = models.TextField(default=None)