from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.templatetags.rest_framework import data
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth import get_user_model
from budget.serializers import AccountDateDetailSerializer
from budget.utils import make_account_date_model_instance
from budget.models import AccountDateDetailModel, AccountDateModel
import logging

logger = logging.getLogger("A")


class DateDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        date = request.query_params.get("date")
    
        try:
            date_pk = AccountDateModel.objects.get(user=request.user.pk ,date=date).pk
        except:
            return Response(
                data={"message": "이 유저는 해당 날짜에 작성한 가계부가 조회되지 않습니다."},
                status=status.HTTP_404_NOT_FOUND,
            )

        qs = AccountDateDetailModel.objects.filter(user=request.user.pk, date=date_pk).order_by("time")
        if len(qs) == 0:
            return Response(
                data={"message": "이 유저는 해당 날짜에 작성한 가계부가 조회되지 않습니다."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = AccountDateDetailSerializer(qs, many=True)
        response_data = self.parse_serializer_to_response(serializer.data, date)

        return Response(data=response_data, status=status.HTTP_200_OK)

    def post(self, request):
        User = get_user_model()
        user_pk = User.objects.get(pk=request.user.pk).pk

        date = request.data[0]["date"]
        date_pk = make_account_date_model_instance(date, user_pk, blank=True).pk

        data = self.make_data_to_optimizer(user_pk, date_pk)

        serializer = AccountDateDetailSerializer(
            data=data,
            context={"request": request},
            many=True,
        )

        return self.valid_save_model(serializer, date, user_pk)

    def put(self, request):
        # user id 파싱
        User = get_user_model()
        user_id = User.objects.get(pk=request.user.pk).pk

        # date 파싱. 0번째 date가 없으면 데이터가 없으므로 모두 삭제 요청으로 인지
        date = request.data[0]["date"]

        try:
            date_id = AccountDateModel.objects.get(user=user_id, date=date).pk
        except:
            raise ValidationError("잘못된 요청입니다.")

        # 해당 날짜의 query 모두 삭제
        queryset = AccountDateDetailModel.objects.filter(user=user_id, date=date_id)
        queryset.delete()

        data = self.make_data_to_optimizer(user_id, date_id)

        serializer = AccountDateDetailSerializer(
            data=data,
            context={"request": request},
            many=True,
        )
        return self.valid_save_model(serializer, date, user_id)

    def make_data_to_optimizer(self, user_pk, date_pk):
        """
        Change the data to fit into Serializer.
        """
        data = self.request.data

        if "delete" in data[0].keys():
            return Response(status=status.HTTP_204_NO_CONTENT)

        for idx, _ in enumerate(data):
            data[idx]["user"] = user_pk
            data[idx]["date"] = date_pk

            tag_to_serializer = self.parse_request_to_serializer(data[idx])
            data[idx]["tag"] = tag_to_serializer
        return data

    def valid_save_model(self, serializer, date, user_pk):
        """
        serializer 유효성 검사 및 모델 저장 / 업데이트
        """
        if serializer.is_valid():
            serializer.save()
            try:
                response_data = self.parse_serializer_to_response(serializer.data, date)
                self.save_summary_account_date_model(date, response_data, user_pk)
                return Response(data=response_data, status=status.HTTP_201_CREATED)
            except:
                return Response(
                    data=serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST,
                )
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def save_summary_account_date_model(date, data, user_pk):
        """
        make summary value in account date model.

        """
        income_summary = 0
        spending_summary = 0
        for dt in data:
            income_summary += int(dt["income"])
            spending_summary += int(dt["spending"])

        make_account_date_model_instance(
            date, user_pk, income_summary, spending_summary
        )

    @staticmethod
    def parse_request_to_serializer(data):
        """
        Make tag(str) in request data To {"tag" : tag"}(dict) for serializer

        """
        tag_to_serializer = []

        temp = data["tag"]
        for i in temp:
            tag_to_serializer.append({"tag": i})

        return tag_to_serializer

    @staticmethod
    def parse_serializer_to_response(data, date):
        """
        make serializer data to response data
        reverse method about parse_request_to_serializer

        """
        try:
            for idx, value in enumerate(data):
                if "user" in data[idx].keys():
                    del data[idx]["user"]
                    
                data[idx]["tag"] = [tag_dict["tag"] for tag_dict in value["tag"]]
                data[idx]["date"] = date
            return data
        except:
            raise ValidationError("tag 정보 parsing error 입니다.")
