from datetime import datetime
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from chart.serializers import TagGetSerializer
from budget.models import TagModel, TagSummaryModel
from logging import getLogger
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

logger = getLogger("A")


class TagTopTenView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        st_month, ed_month = self.make_datetime_dataset(
            request.query_params.get("st_month"), request.query_params.get("ed_month")
        )
        self.valid_month_gap(st_month,ed_month)
        
        user_id = request.user.pk
        query_set = TagSummaryModel.objects.filter(
            user_id=user_id, date__gte=st_month, date__lte=ed_month
        )
        
        try:
            serializer = TagGetSerializer(instance=query_set, many=True)
            return_data = self.make_response_data(serializer.data, request)
            return Response(data=return_data, status=status.HTTP_200_OK)
        except:
            return Response(data={"message": "data 가 존재하지 않습니다."})

    def make_response_data(self, data, request):
        temp = {"spending": "spending_top_ten", "income": "income_top_ten"}
        return_data = {
            "spending_top_ten": {},
            "income_top_ten": {},
        }

        for i in data:
            tag_id = i["tag_id"]
            tag_name = TagModel.objects.get(id=tag_id).tag

            if int(i["spending"]):
                x = "spending"
            elif int(i["income"]):
                x = "income"

            try:
                return_data[temp[x]][tag_name] += int(i[x])
            except:
                return_data[temp[x]][tag_name] = int(i[x])

            return_data[temp[x]] = dict(
                sorted(
                    return_data[temp[x]].items(),
                    key=lambda item: item[1],
                    reverse=True
                )
            )            
        return_data = self.del_zero_data(return_data)
        return_data = self.make_top_ten(return_data)
        
        if request.META.get("HTTP_CHART_DATATYPE") == "percent":
            return_data = self.make_persent_data(return_data)
        
        return return_data
    
    @staticmethod
    def make_persent_data(return_data):
        sum_spending = sum(list(return_data["spending_top_ten"].values()))
        sum_income = sum(list(return_data["income_top_ten"].values()))
        
        spending_keys = list(return_data["spending_top_ten"].keys())
        income_keys = list(return_data["income_top_ten"].keys())
        
        for i in spending_keys:
            return_data["spending_top_ten"][i] = str(round(return_data["spending_top_ten"][i] / sum_spending * 100,2)) + "%"
        
        for i in income_keys:
            return_data["income_top_ten"][i] = str(round(return_data["income_top_ten"][i] / sum_income * 100,2)) + "%"
            
        return return_data

    @staticmethod
    def valid_month_gap(st_date, ed_date):
        date_gap = ed_date - st_date
        
        if date_gap.days < 0:
            raise ValidationError("그래프의 시작날짜가 종료날짜보다 큽니다.")
        
        if date_gap.days > 365:
            raise ValidationError("그래프는 총 12개월 간격까지 보여줄 수 있습니다.")
    
    @staticmethod
    def make_datetime_dataset(st_month, ed_month):
        date_format = "%Y-%m"
        st_month = datetime.strptime(st_month, date_format)
        ed_month = datetime.strptime(ed_month, date_format)

        return st_month, ed_month

    
    @staticmethod
    def del_zero_data(return_data):
        try:
            for i in list(return_data["spending_top_ten"].keys()):
                if return_data["spending_top_ten"][i] == 0:
                    del return_data["spending_top_ten"][i]
        except:
            pass
        
        try:
            for i in list(return_data["income_top_ten"].keys()):
                if return_data["income_top_ten"][i] == 0:
                    del return_data["income_top_ten"][i]
        except:
            pass
        
        return return_data

    @staticmethod
    def make_top_ten(return_data):
        temp = ["income_top_ten", "spending_top_ten"]
        for i in temp:
            if len(return_data[i]) > 10:
                temp_2 = return_data[i]
                del return_data[i]
                return_data[i] = {key:temp_2[key] for key in list(temp_2.keys())[:10]}
        
        return return_data