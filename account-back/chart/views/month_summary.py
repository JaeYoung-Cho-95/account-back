from urllib import response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from datetime import datetime
from budget.models import AccountDateModel
from rest_framework import status
from logging import getLogger

logger = getLogger("A")

class monthSummary(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_pk = request.user.pk
        st_date = request.query_params.get("st_month")
        ed_date = request.query_params.get("ed_month")
        self.cal_date(st_date, ed_date)

        return Response(
            data=self.make_response_data(user_pk, st_date, ed_date),
            status=status.HTTP_200_OK
        )
        
    @staticmethod
    def cal_date(st_month, ed_month):
        date_format = "%Y-%m"

        st_month = datetime.strptime(st_month, date_format)
        ed_month = datetime.strptime(ed_month, date_format)

        month_gap = ed_month - st_month

        if month_gap.days > 365:
            raise ValidationError("그래프는 총 12개월 간격까지 보여줄 수 있습니다.")

        if month_gap.days < 0:
            raise ValidationError("그래프의 시작날짜가 종료날짜보다 큽니다.")

    @staticmethod
    def make_response_data(user_pk, st_date, ed_date):
        st_year, st_month = list(map(int, st_date.split("-")))
        ed_year, ed_month = list(map(int, ed_date.split("-")))

        response_data = []
        while True:
            query_set = AccountDateModel.objects.filter(
                user=user_pk,
                date__year=str(st_year),
                date__month=str(st_month),
            )
            
            response_data.append({})
            response_data[-1]["date"] = f"{st_year}-{st_month}"
            
            response_data[-1]["left_money"] = 0
            for i in query_set:
                response_data[-1]["left_money"] += int(i.left_money)

            if (st_year == ed_year) and (st_month == ed_month):
                break
            
            st_month += 1
            if st_month >= 13:
                st_month = 1
                st_year += 1
            
        return response_data