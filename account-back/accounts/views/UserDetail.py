from email import message
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.authentication import JWTAuthentication
from accounts.serializers import UserSerializer

class UserDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self,request):
        request_email = request.query_params.get("email")
        User_model = get_user_model()
        
        user_qs = User_model.objects.filter(email=request_email).first()    
        if not user_qs:
            return Response(message={
                'message': "사용자가 존재하지 않습니다"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        user_serializer = UserSerializer(user_qs).data
        return Response(user_serializer, status=status.HTTP_200_OK)
        