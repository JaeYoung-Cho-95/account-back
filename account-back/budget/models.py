import datetime
from django.db import models
from django.conf import settings


# Create your models here.
class TimeTempleteModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True


class AccountDateModel(TimeTempleteModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    datetime = models.DateTimeField(blank=False)
    income_summary = models.DecimalField(max_digits=11, decimal_places=0, default=0)
    spending_summary = models.DecimalField(max_digits=11, decimal_places=0, default=0)
    left_money = models.DecimalField(max_digits=11, decimal_places=0, default=0)
    
    class Meta:
        ordering : ['-datetime']
    
    def __str__(self):
        return f"{self.datetime} 남은 돈 : {self.left_money}"
    
    
class AccountDateDetailModel(TimeTempleteModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.ForeignKey('AccountDateModel', on_delete=models.CASCADE)
    tag = models.ManyToManyField("TagModel", blank=True)
    
    time = models.TimeField(default=datetime.time(0,0))
    income = models.DecimalField(max_digits=11, decimal_places=0, default=0)
    spending = models.DecimalField(max_digits=11, decimal_places=0, default=0)
    content = models.CharField(max_length=50, blank=True)
    
    class Meta:
        ordering : ['time']


class TagModel(models.Model):
    tag = models.CharField(max_length=10, unique=True)