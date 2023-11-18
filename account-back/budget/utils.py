from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from .models import AccountDateModel
from .serializers import AccountDateSerializer
import datetime
import logging

logger = logging.getLogger("A")


def make_account_date_model_instance(
    request, user_pk, income_summary=0, spend_summary=0
):
    date = request.data[0].get("date")

    # letf money 계산을 위해 최근 db 조회
    accountdate_instance = (
        AccountDateModel.objects.filter(user=user_pk).order_by("-date").first() or False
    )

    # db에 조회 되면 해당 값으로 leftmoney 계산
    if accountdate_instance:
        leftmoney = accountdate_instance.left_money + income_summary - spend_summary
    else:
        leftmoney = 0 + income_summary - spend_summary

    data = {
        "user": user_pk,
        "date": date,
        "income_summary": str(income_summary),
        "spending_summary": str(spend_summary),
        "left_money": str(leftmoney),
    }

    # 기존에 날짜와 동일한 instance 가 있으면 업데이트, 없으면 생성
    try:
        accountdate_instance = AccountDateModel.objects.get(date=date)
    except:
        accountdate_instance = None

    accountdate_serializer = AccountDateSerializer(
        instance=accountdate_instance, data=data
    )

    if accountdate_serializer.is_valid():
        return accountdate_serializer.save()

    raise ValidationError([{'date': ['잘못된 날짜 형식입니다.']}])