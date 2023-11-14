from rest_framework.serializers import ModelSerializer, ListField, CharField
from .models import AccountDateModel, AccountDateDetailModel, TagModel
import datetime


class AccountDateSerializer(ModelSerializer):
    class Meta:
        model = AccountDateModel
        fields = [
            "date",
            "income_summary",
            "spending_summary",
            "left_money",
        ]


class AccountDateDetailSerializer(ModelSerializer):
    tag = ListField(child=CharField(max_length=10), max_length=5)
    time = CharField(max_length=2)

    class Meta:
        model = AccountDateDetailModel
        fields = ["date", "tag", "time", "income", "spending", "content"]

    def create(self, validated_data):
        instances = []

        date = datetime.date(*map(int, validated_data[0]["date"].split("-")))
        instance = self.make_month_model_instance(date)

        spend_total, income_total = 0, 0

        for data in validated_data:
            # spend_total 및 income_total 합
            spend_total += data["spending"]
            income_total += data["income"]

            # time string > datetime type 변환
            time = map(int, data.get("time", 0))
            time = datetime.time(time)
            data["time"] = time

            # 외래키 정보 파싱
            tag_data = data.pop("tag", [])

            # detail model 생성
            instance = AccountDateDetailModel.objects.create(**data)
            instance.date.add()
            # tag instacne 생성 후 외래키 연결
            for tag in tag_data:
                tag, _ = TagModel.objects.get_or_create(tag=tag)
                instance.tag.add(tag)
            
            instances.append(instance)

        return instances

    def make_account_date_model_instance(self, date, income_summary=0, spend_summary=0):
        user = self.context.get("request").user

        accountdate_instance = (
            AccountDateModel.objects.filter(user=user).order_by("-date").first() or 0
        )
        if accountdate_instance:
            leftmoney = accountdate_instance.left_money
        else:
            leftmoney = 0

        data = {
            "user": user,
            "date": date,
            "income_summary": income_summary,
            "spend_summary": spend_summary,
            "left_money": leftmoney,
        }

        detail_serializer = AccountDateSerializer(data)
        if detail_serializer.is_valid():
            instance = AccountDateModel.objects.get_or_create(detail_serializer.data)
            return instance