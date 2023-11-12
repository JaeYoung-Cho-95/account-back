from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model
import logging

logger = logging.getLogger("A")


class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get("refresh_token")
    
        response, valid_res = self.valid_token(refresh_token, request)
        User = get_user_model()
        
        if not valid_res:
            return response
        
        refresh_token = RefreshToken(refresh_token)
        user = refresh_token["user_id"]
        
        new_refresh_token = RefreshToken.for_user(User.objects.get(id=user))
        
        data = {"access_token": f"{new_refresh_token.access_token}"}
        
        refresh_token.blacklist()
        
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
        return (None, True)
