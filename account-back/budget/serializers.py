from rest_framework.exceptions import ValidationError
from rest_framework.serializers import (
    ModelSerializer,
    CharField,
    PrimaryKeyRelatedField,
)
from rest_framework.exceptions import ValidationError
from .models import AccountDateModel, AccountDateDetailModel, TagModel
from django.contrib.auth import get_user_model
import logging

logger = logging.getLogger("A")


class TagSerializer(ModelSerializer):
    class Meta:
        model = TagModel
        fields = ["tag"]


class AccountDateSerializer(ModelSerializer):
    user = PrimaryKeyRelatedField(queryset=get_user_model().objects.all())

    class Meta:
        model = AccountDateModel
        fields = [
            "user",
            "date",
            "income_summary",
            "spending_summary",
            "left_money",
        ]


class AccountDateDetailSerializer(ModelSerializer):
    user = PrimaryKeyRelatedField(queryset=get_user_model().objects.all())
    date = PrimaryKeyRelatedField(queryset=AccountDateModel.objects.all())
    tag = TagSerializer(many=True)
    time = CharField(max_length=2)

    def __init__(self, **kwargs):
        super(AccountDateDetailSerializer, self).__init__(**kwargs)
        self.spend_total = 0
        self.income_total = 0

    class Meta:
        model = AccountDateDetailModel
        fields = ["user", "date", "tag", "time", "income", "spending", "content"]

    def create(self, validated_data):
        # time string > datetime type 변환
        time = validated_data.get("time", 0)
        validated_data["time"] = f"{time}:00"

        # ManyToMany field tag 정보 파싱
        tag_data = validated_data.pop("tag", [])
        exist_flag = AccountDateDetailModel.objects.filter(**validated_data)

        if len(exist_flag) >= 1:
            raise ValidationError("유저는 이미 해당 날짜에 가계부를 작성하였습니다.")
        else:
            # detail model 생성
            instance = AccountDateDetailModel.objects.create(**validated_data)
            # ManyToMany field tag 연결
            for tag in tag_data:
                tag_instance, _ = TagModel.objects.get_or_create(tag=tag["tag"])
                instance.tag.add(tag_instance)
            return instance

    def validate_tag(self, value):
        if len(value) > 5:
            raise ValidationError("tag 는 5개까지 입력이 가능합니다.")
        return value

    def validate_time(self, value):
        if int(value) < 0 or int(value) > 24:
            raise ValidationError("시간은 0 ~ 24 사이의 숫자만 선택이 가능합니다.")

        return value
