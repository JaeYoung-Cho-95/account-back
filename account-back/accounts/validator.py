from signal import raise_signal
from django.core.validators import EmailValidator
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueValidator
from .models import User


def validate_password(password):
    error = serializers.ValidationError(
        "비밀번호 생성 조건 : 8 ~ 20 글자, 1개 이상 숫자, 1개 이상 소문자, 1개 이상 대문자, 특수문자 !@#$()%^&* 중 1개 이상"
    )

    if len(password) < 8 or len(password) > 20:
        raise error
    if not any(char.isdigit() for char in password):
        raise error
    if not any(char.isalpha() for char in password):
        raise error
    if not any(char.isupper() for char in password):
        raise error
    if not any(char in "!@#$%^&*()" for char in password):
        raise error

    return password


def validate_email(email):
    if User.objects.filter(email=email).exists():
        raise serializers.ValidationError("중복된 이메일입니다.")

    validator = EmailValidator()
    try:
        validator(email)
    except serializers.ValidationError:
        raise serializers.ValidationError("유효하지 않은 이메일 주소입니다.")

    return email


def validate_nickname(nickname):
    if User.objects.filter(nickname=nickname).exists():
        raise serializers.ValidationError("중복된 닉네임입니다.")

    if len(nickname) > 20 or len(nickname) < 2:
        raise serializers.ValidationError("별명은 2~20 글자입니다.")

    return nickname


def validate_username(username):
    if len(username) > 5 or len(username) < 2:
        raise serializers.ValidationError("이름은 2글자 ~ 5글자 이하입니다.")

    return username
