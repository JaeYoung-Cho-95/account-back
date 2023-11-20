import datetime
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from .models import AccountDateModel
from .serializers import AccountDateSerializer

import logging

logger = logging.getLogger("A")


def make_account_date_model_instance(
    date, user_pk, income_summary=0, spend_summary=0, blank=False
):
    User = get_user_model()
    user_instance = User.objects.get(pk=user_pk)
    user_last_date = user_instance.last_date
    input_date = datetime.date(*list(map(int, date.split("-"))))
    
    # 추가하는 가계부 내용의 날짜가 가장 최신인 경우
    if input_date >= user_last_date:
        if blank:
            left_money = 0
            return AccountDateSave(
                user_pk, date, income_summary, spend_summary, left_money
            )

        # left money 계산을 위해 최근 db 조회
        accountdate_instance = (
            AccountDateModel.objects.filter(user=user_pk, date__lt=input_date).first()
            or False
        )

        # db에 조회 되면 해당 값으로 leftmoney 계산
        left_money = calculte_left_money(
            accountdate_instance, income_summary, spend_summary
        )

        # user 최신 date 날짜 최신화
        update_user_last_date(user_pk, date)

        # account_date 저장
        return AccountDateSave(user_pk, date, income_summary, spend_summary, left_money)

    # 추가하는 가계부 내용의 날짜가 최신이 아닌 경우
    else:
        if blank:
            left_money = 0
            return AccountDateSave(
                user_pk, date, income_summary, spend_summary, left_money
            )

        # 입력 가계부 날짜 직전의 account_instance 모델 가지고 와서 left money 계산
        try:
            accountdate_instance = AccountDateModel.objects.filter(
                user=user_pk, date__lt=input_date
            )[0]
            left_money = (
                accountdate_instance.left_money + income_summary - spend_summary
            )
        except:
            left_money = 0 + income_summary - spend_summary

        # account_date 저장
        account_date_instance = AccountDateSave(
            user_pk, date, income_summary, spend_summary, left_money
        )
        
        # left money 업데이트
        left_money = int(account_date_instance.left_money)
        AccountDateModel_qs = AccountDateModel.objects.filter(
            user=user_pk, date__gt=input_date
        ).order_by("date")

        for instance in AccountDateModel_qs:
            left_money = (
                int(left_money)
                + int(instance.income_summary)
                - int(instance.spending_summary)
            )
            instance.left_money = str(left_money)
            instance.save()


def AccountDateSave(user_pk, date, income_summary, spend_summary, left_money):
    data = {
        "user": user_pk,
        "date": date,
        "income_summary": str(income_summary),
        "spending_summary": str(spend_summary),
        "left_money": str(left_money),
    }

    # 기존에 날짜와 동일한 instance 가 있으면 업데이트, 없으면 생성
    try:
        date = datetime.date(*list(map(int, date.split("-"))))
        accountdate_instance = AccountDateModel.objects.get(user_id=user_pk, date=date)
    except:
        accountdate_instance = None

    accountdate_serializer = AccountDateSerializer(
        instance=accountdate_instance, data=data
    )

    if accountdate_serializer.is_valid():
        # user 정보에서 last_date 값 업데이트
        return accountdate_serializer.save()

    raise ValidationError(accountdate_serializer.errors)


def calculte_left_money(accountdate_instance, income_summary, spend_summary):
    if accountdate_instance:
        left_money = (
            int(accountdate_instance.left_money) + income_summary - spend_summary
        )
    else:
        left_money = 0 + income_summary - spend_summary

    return left_money


def update_user_last_date(user_pk, date):
    """
    User 정보의 last_date 값을 업데이트
    """
    User = get_user_model()
    user = User.objects.get(pk=user_pk)
    user.last_date = date
    user.save()
