from rest_framework.response import Response
from accounts.serializers import UserSerializer
from budget.models import AccountDateModel
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.views import APIView
from datetime import date


User = get_user_model()


class UserCreateView(APIView):
    def post(self, request):
        data = request.data
        
        serializer = UserSerializer(data=data)
        
        if serializer.is_valid():
            serializer.save()
            # user 생성 후 user에게 당일 기준 Datemodel instance 생성
            self.make_budget_Account_Date_model(serializer.data)
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    @staticmethod
    def make_budget_Account_Date_model(data):
        User = get_user_model()
        user_instance = User.objects.get(email=data['email'])
        
        data = {
            'user': user_instance,
            'date': str(date.today()),
            'income_summary' : '0',
            'spending_summary' : '0',
            'left_money' : '0'
        }
        
        return AccountDateModel.objects.create(**data)
        