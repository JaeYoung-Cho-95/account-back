from datetime import datetime, timedelta
import stat
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken


class userLogOutView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.COOKIES.get("refresh_token")
        
        if not refresh_token:
            return Response(
                data={"message": "refresh token 이 존재하지 않습니다."},
                status=status.HTTP_401_UNAUTHORIZED,
            )
            
        try:
            refresh_token = RefreshToken(refresh_token)
            refresh_token.blacklist()
        except:
            return Response(
                data={"message": "잘못된 refresh token 정보입니다."},
                status=status.HTTP_401_UNAUTHORIZED
            )

        response = Response(data={"message": "로그아웃 되었습니다."}, status=status.HTTP_200_OK)
        expire_time = datetime.now() + timedelta(seconds=1)
        response.set_cookie(
            "refresh_token", "", httponly=True, secure=True, expires=expire_time
        )

        return response
