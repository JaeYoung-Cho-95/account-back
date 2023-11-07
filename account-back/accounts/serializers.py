from .models import User
from .validator import (
    validate_username,
    validate_password,
    validate_email,
    validate_nickname,
)
from rest_framework import serializers

import logging

logger = logging.getLogger("A")


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(validators=[validate_email])
    username = serializers.CharField(validators=[validate_username])
    nickname = serializers.CharField(validators=[validate_nickname])
    password = serializers.CharField(write_only=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ["email", "username", "nickname", "password"]

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
