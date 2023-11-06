from .models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "username", "nickname", "password"]
        extra_kwargs = {
            'password':{"write_only": True}
        }
        

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data["email"],
            username=validated_data["username"],
            nickname=validated_data["nickname"],
            password=validated_data["password"],
        )
        return user
