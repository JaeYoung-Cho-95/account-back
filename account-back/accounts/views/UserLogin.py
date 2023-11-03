from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from accounts.serializers import UserSerializer
from django.contrib.auth import get_user_model
from rest_framework import status, views
from django.contrib.auth.hashers import check_password

class UserLoginView(views.APIView):
    def post(self,request):
        # 유저 정보 파싱
        user, password = self.parse_user_info(request)
        
        # user 존재 X
        if not user:
            return Response(
                {"message": "존재하지않는 아이디입니다."}, 
                status=status.HTTP_400_BAD_REQUEST
                )
        
        # 비밀번호 일치 X
        if not check_password(password, user.password):
            return Response(
                {"message": "비밀번호가 일치하지않습니다.."}, 
                status=status.HTTP_400_BAD_REQUEST
                )
        
        try:
            return self.make_token_with_cookie(user)
        except:
            return Response(
                {"message": "로그인에 실패하였습니다. 재시도해주세요."},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @staticmethod
    def parse_user_info(request):
        email = request.data.get("email")
        password = request.data.get("password")
        
        # 데이터 추출
        User = get_user_model()
        user = User.objects.filter(email=email).first()
        
        return user, password
    
    
    @staticmethod
    def make_token_with_cookie(user):
        token = TokenObtainPairSerializer.get_token(user)
        refresh_token = str(token)
        access_token = str(token.access_token)
        response = Response(
                {
                    "user": UserSerializer(user).data,
                    "message": "로그인 성공",
                    "jwt_token": {
                        "access_token": access_token,
                        "refresh_token": refresh_token
                    },
                },
                status=status.HTTP_200_OK
            )

        response.set_cookie("access_token", access_token, httponly=True)
        response.set_cookie("refresh_token", refresh_token, httponly=True)

        return response