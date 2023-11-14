from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from rest_framework import status
from budget.serializers import AccountDateDetailSerializer

class DateDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self,request):
        serializer =  AccountDateDetailSerializer(request.data, context={'request': request} ,many=True)
        if serializer.is_valid():
            serializer.save()
            
            return Response(data={
                serializer.data
            }, status = status.HTTP_201_CREATED)
            
    
    def put(self,request):
        pass
    
    def delete(self,request):
        pass
    