from rest_framework.serializers import ModelSerializer
from .models import AccountDateModel

class AccountDateSerializer(ModelSerializer):
    class Meta:
        model = AccountDateModel
        fields = [
            "date",
            "income_summary",
            "spending_summary",
            "left_money",
            ]