from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.hashers import check_password
from accounts.serializers import UserSerializer
from accounts.views.utils.parsing import Parsing

import logging
logger = logging.getLogger("A")

class UserDetailView(APIView, Parsing):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_instance, _ = self.parse_user_info(request)

        if user_instance != request.user:
            return Response(
                data={"message": "본인계정에 대한 조회만 가능합니다."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if not user_instance:
            return Response(
                data={"message": "사용자가 존재하지 않습니다"}, status=status.HTTP_404_NOT_FOUND
            )

        user_serializer = UserSerializer(user_instance).data
        return Response(user_serializer, status=status.HTTP_200_OK)

    def patch(self, request):
        logger.info(request.data)
        user_instance, password = self.parse_user_info(request)

        _response, valid_res = self.valid_user(user_instance, request, password)

        if valid_res:
            data = self.pop_email_username(request.data)

            if "current_password" in data.keys():
                data = self.pop_change_password(data)

            serializer = UserSerializer(
                user_instance, data, context={"request": request}, partial=True
            )

            if serializer.is_valid():
                serializer.save()
                return Response(data=serializer.data, status=status.HTTP_200_OK)

            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        return _response

    def delete(self, request):
        user_instance, password = self.parse_user_info(request)
        _response, valid_res = self.valid_user(user_instance, request, password)
        if valid_res:
            user_instance.delete()
            return Response(
                data={"message": "회원탈퇴가 정상적으로 되었습니다."},
                status=status.HTTP_204_NO_CONTENT,
            )
        return _response

    @staticmethod
    def valid_user(user_instance, request, password=None):
        if not user_instance:
            return (
                Response(
                    {"message": "존재하지않는 이메일입니다."}, status=status.HTTP_400_BAD_REQUEST
                ),
                False,
            )
        if not check_password(password, user_instance.password):
            return (
                Response(
                    {"message": "비밀번호가 일치하지않습니다."}, status=status.HTTP_401_UNAUTHORIZED
                ),
                False,
            )

        if user_instance == request.user:
            return None, True
        return (
            Response(
                {"message": "access token 과 유저의 정보가 일치하지 않습니다."},
                status=status.HTTP_401_UNAUTHORIZED,
            ),
            False
        )