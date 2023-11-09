from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from accounts.serializers import UserSerializer
from accounts.views.utils.parsing import Parsing

import logging

logger = logging.getLogger("A")


class UserDetailView(APIView, Parsing):
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
        user_instance, _ = self.parse_user_info(request)

        # 유저정보 인증
        _response, valid_res = self.valid_user(user_instance, request)

        # 인증 완료
        if valid_res:
            # email 과 username 은 변경하지 않음
            data = self.pop_email_username(request.data)
            serializer = UserSerializer(user_instance, data, context={"request": request}, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(data=serializer.data, status=status.HTTP_200_OK)
            
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )
        # 인증 실패
        return _response

    def delete(self, request):
        # 유저 정보 파싱
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

        # 회원탈퇴는 비밀번호 검증도 진행
        if (request.method == "DELETE") and (
            not check_password(password, user_instance.password)
        ):
            return (
                Response(
                    {"message": "비밀번호가 일치하지않습니다."}, status=status.HTTP_401_UNAUTHORIZED
                ),
                False,
            )

        # 요청자의 username 과 삭제하려는 user_instance의 username 가 동일해야함.
        if user_instance == request.user:
            return None, True