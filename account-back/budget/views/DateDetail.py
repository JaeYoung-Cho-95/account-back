from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth import get_user_model
from budget.serializers import AccountDateDetailSerializer
from budget.utils import make_account_date_model_instance
import logging

logger = logging.getLogger("A")


class DateDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        User = get_user_model()
        user_instance = User.objects.get(pk=request.user.pk)
        user_pk = user_instance.pk
        
        account_date_instance = make_account_date_model_instance(request, user_pk)
        
        date_pk = account_date_instance.pk

        for idx, _ in enumerate(request.data):
            request.data[idx]["user"] = user_pk
            request.data[idx]["date"] = date_pk
            
            tag_to_serializer = self.parse_request_to_serializer(request.data[idx])
            request.data[idx]['tag'] = tag_to_serializer

        serializer = AccountDateDetailSerializer(
            data=request.data,
            context={"request": request},
            many=True,
        )

        if serializer.is_valid():
            try:
                serializer.save()
                response_data = self.parse_serializer_to_response(serializer.data)
                return Response(data=response_data, status=status.HTTP_201_CREATED)
            except:
                return Response(
                    data=[{'message': ["이미 존재하는 데이터에 대한 post 요청입니다."]}],
                    status=status.HTTP_400_BAD_REQUEST,
                )
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @staticmethod
    def parse_request_to_serializer(data):
        """
        Make tag(str) in request data To {"tag" : tag"}(dict) for serializer

        Args:
            data (dict): request.data

        Returns:
            data (dict): validated data for serializer   
        """        
        tag_to_serializer = []
        
        temp = data['tag']
        for i in temp:
            tag_to_serializer.append(
                {"tag": i}
            )
            
        return tag_to_serializer
        
    @staticmethod
    def parse_serializer_to_response(data):
        """
        make serializer data to response data
        reverse method about parse_request_to_serializer
    
        Args:
            data (dict): serializer data

        Returns:
            data (dict) : respoonse data for frontend
        """        
        for idx, value in enumerate(data):
            data[idx]["tag"] = [tag_dict["tag"] for tag_dict in value["tag"]]
        
        return data