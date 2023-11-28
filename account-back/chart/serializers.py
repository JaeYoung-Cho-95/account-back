from rest_framework.serializers import ModelSerializer
from budget.models import AccountDateModel

class DateGetSerializer(ModelSerializer):
    class Meta:
        model = AccountDateModel
        fields = ["date","left_money"]
    