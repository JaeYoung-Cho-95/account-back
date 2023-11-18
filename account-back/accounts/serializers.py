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
        fields = ["email", "username", "nickname", "password", "profile_image"]
     
    def __init__(self, *args, **kwargs):
        super(UserSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request', None)
        
        if request and getattr(request, 'method', None) == 'PATCH':
            for field_name in self.fields:
                field = self.fields[field_name]
                field.required = False
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        if password:
            instance.set_password(password)
        
        instance.save()
        
        return instance
    
    def validate_profile_image(self, value):
        pass