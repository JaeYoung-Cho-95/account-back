from .models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['userID', 'username', 'phone_number', 'email','password']
    
    def create(self, validated_data):
        user = User.objects.create_user(
            userID = validated_data['userID'],
            username = validated_data['username'],
            phone_number = validated_data['phone_number'],
            email = validated_data['email'],
            password = validated_data["password"],
        )
        return user