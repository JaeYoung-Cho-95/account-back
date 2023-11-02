import logging
from accounts.serializers import UserSerializer

from django.contrib.auth import get_user_model
from django.conf import settings
from rest_framework import generics

User = get_user_model()

# Create your views here.
class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer