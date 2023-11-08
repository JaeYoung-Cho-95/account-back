from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.authentication import JWTAuthentication
from accounts.serializers import UserSerializer

import logging

logger = logging.getLogger("A")


class UserDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        request_email = request.query_params.get("email")
        User_model = get_user_model()

        user_qs = User_model.objects.filter(email=request_email).first()
        if not user_qs:
            return Response(
                data={"message": "사용자가 존재하지 않습니다"}, status=status.HTTP_404_NOT_FOUND
            )

        user_serializer = UserSerializer(user_qs).data
        return Response(user_serializer, status=status.HTTP_200_OK)

    def patch(self, request):
        # 유저정보 query set 파싱
        User_model = get_user_model()
        user = User_model.objects.filter(email=request.data.get("email")).first()
        if not user:
            return Response(
                data={"message": "존재하지 않는 email 입니다."},
                status=status.HTTP_400_BAD_REQUEST,
            )
            
        # email 과 username 은 변경하지 않음
        data = request.data.copy()
        data.pop('email', None)
        data.pop('username', None)
        
        serializer = UserSerializer(user, data, context={'request': request}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                data={"message": "정상적으로 정보가 변경됐습니다."}, 
                status=status.HTTP_200_OK
            )

        return Response(
            data=serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )