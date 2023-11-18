from rest_framework.response import Response
from accounts.serializers import UserSerializer

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.views import APIView


User = get_user_model()


class UserCreateView(APIView):
    def post(self, request):
        data = request.data
        
        serializer = UserSerializer(data=data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)