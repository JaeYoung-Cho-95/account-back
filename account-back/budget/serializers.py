from venv import logger
from rest_framework.serializers import ModelSerializer, ListField, CharField
from .models import AccountDateModel, AccountDateDetailModel, TagModel
import datetime

import logging

logger = logging.getLogger("A")


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
    date = CharField(max_length=20)
    tag = ListField(child=CharField(max_length=10), max_length=5)
    time = CharField(max_length=2)

    class Meta:
        model = AccountDateDetailModel
        fields = ["date", "tag", "time", "income", "spending", "content"]

    def create(self, validated_data):
        instances = []

        logger.info("*"*30)
        logger.info(validated_data)
        logger.info("*"*30)
        
        date = datetime.date(*map(int, validated_data[0]["date"].split("-")))
        date_instance = self.make_account_date_model_instance(date)

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
            
            # DateDetail model의 date column 에 date_instance 외래키 연결
            instance.date.add(date_instance)
            
            # DateDetail model의 tag column 에 tag_instance 외래키 연결
            for tag in tag_data:
                tag, _ = TagModel.objects.get_or_create(tag=tag)

                instance.tag.add(tag)
            
            instances.append(instance)

        # incomde_total , spend_total 결과를 넣어서 업데이트 하기
        self.make_account_date_model_instance(date, income_total, spend_total)
        
        return instances

    def make_account_date_model_instance(self, date, income_summary=0, spend_summary=0):
        user = self.context.get("request").user

        accountdate_instance = AccountDateModel.objects.filter(user=user).order_by("-date").first() or False
        if accountdate_instance:
            leftmoney = accountdate_instance.left_money + income_summary - spend_summary
        else:
            leftmoney = 0 + income_summary - spend_summary

        data = {
            "user": user,
            "date": date,
            "income_summary": income_summary,
            "spend_summary": spend_summary,
            "left_money": leftmoney,
        }

        detail_serializer = AccountDateSerializer(data)
        if detail_serializer.is_valid():
            instance, _ = AccountDateModel.objects.get_or_create(**detail_serializer.data)
            return instance