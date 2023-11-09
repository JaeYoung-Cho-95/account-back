from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import AnonymousUser
import logging

logger = logging.getLogger("A")


class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        # 쿠키에서 refresh token 가지고 오기
        refresh_token = request.COOKIES.get("refresh_token")

        # 각종 사용자 및 토큰 정보 인증
        response, valid_res = self.valid_token(refresh_token, request)
        
        # 인증 실패시 에러 메시지 및 상태코드 응답
        if not valid_res:
            return response
        
        # 기존 refresh token 을 이용해서 access_token 발급
        refresh_token = RefreshToken(refresh_token)
        data = {"access": f"{refresh_token.access_token}"}
        # 기존 refresh token 은 blacklist 에 추가
        refresh_token.blacklist()

        # 새로운 refresh token 발급
        new_refresh_token = RefreshToken.for_user(request.user)
        response = Response(data=data, status=status.HTTP_200_OK)
        response.set_cookie(
            "refresh_token", f"{new_refresh_token}", httponly=True, secure=True
        )

        return response

    def get_serializer(self, *args, **kwargs):
        return TokenRefreshSerializer(*args, **kwargs)

    @staticmethod
    def valid_token(refresh_token, request):
        if not refresh_token:
            return (
                Response(
                    {"message": "refresh token 이 존재하지 않습니다."},
                    status=status.HTTP_401_UNAUTHORIZED,
                ),
                False,
            )

        try:
            refresh_token = RefreshToken(refresh_token)
        except:
            return (
                Response(
                    {"message": "잘못된 refresh token 입니다."},
                    status=status.HTTP_401_UNAUTHORIZED,
                ),
                False,
            )

        if isinstance(request.user, AnonymousUser):
            return (
                Response(
                    {"message": "로그인이 필요합니다."},
                    status=status.HTTP_401_UNAUTHORIZED,
                ),
                False,
            )

        return (None, True)
