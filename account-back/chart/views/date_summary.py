from datetime import datetime
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from budget.models import AccountDateModel
from chart.serializers import DateGetSerializer
from logging import getLogger

logger = getLogger("A")

class dateSummary(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self,request):
        user_pk = request.user.pk
        st_date = request.query_params.get("st_date")
        ed_date = request.query_params.get("ed_date")
        
        self.cal_date(st_date, ed_date)
        
        date_qeuryset = AccountDateModel.objects.filter(user=user_pk, date__lte=ed_date, date__gte=st_date)
        
        serializer = DateGetSerializer(date_qeuryset, many=True)
        
        try:
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(data=serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)
    
    @staticmethod
    def cal_date(st_date, ed_date):
        date_format = "%Y-%m-%d"
        
        st_date = datetime.strptime(st_date,date_format)
        ed_date = datetime.strptime(ed_date,date_format)
        date_gap = ed_date - st_date
        
        if date_gap.days < 0:
            raise ValidationError("그래프의 시작날짜가 종료날짜보다 큽니다.")
        
        if date_gap.days > 365:
            raise ValidationError("그래프는 총 365일 간격까지 보여줄 수 있습니다.")
