from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from budget.models import AccountDateModel
from budget.serializers import AccountDateSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
import logging

logger = logging.getLogger("A")


class DateSummaryView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        qs = AccountDateModel.objects.filter(user=request.user)

        if not qs:
            return Response(
                data={"message": "유저 정보가 존재하지 않습니다."}, status=status.HTTP_404_NOT_FOUND
            )

        request_date_year, request_date_month = request.query_params.get("date").split("-")
        qs = qs.filter(date__year=request_date_year, date__month=request_date_month)
        if not qs:
            return Response(
                data={"message": "요청된 날짜에 대한 data가 존재하지 않습니다."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = AccountDateSerializer(qs, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)