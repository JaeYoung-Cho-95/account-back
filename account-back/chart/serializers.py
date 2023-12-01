from rest_framework.serializers import ModelSerializer
from budget.models import AccountDateModel, TagSummaryModel


class DateGetSerializer(ModelSerializer):
    class Meta:
        model = AccountDateModel
        fields = ["date", "left_money"]


class TagGetSerializer(ModelSerializer):
    class Meta:
        model = TagSummaryModel
        fields = ["tag_id","date", "spending", "income"]
