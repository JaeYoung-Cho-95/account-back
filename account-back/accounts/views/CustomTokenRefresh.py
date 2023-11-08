from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework.response import Response
from rest_framework import status


class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        """
        쿠키에서 리프레시 토큰을 받아 새로운 액세스 토큰을 발급합니다.
        """
        # 쿠키에서 리프레시 토큰을 가져옵니다.
        refresh = request.COOKIES.get("refresh_token", None)

        if refresh is None:
            return Response(
                {"detail": "Refresh token was not provided."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.get_serializer(data={"refresh": refresh})

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(serializer.validated_data, status=status.HTTP_200_OK)

    def get_serializer(self, *args, **kwargs):
        """
        Custom serializer를 반환합니다.
        """
        return TokenRefreshSerializer(*args, **kwargs)
