from django.contrib.auth import authenticate
from rest_framework import serializers

from .models import User


class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "password", "nickname", "name"]
        extra_kwargs = {
            "profile_image": {"required": False},
        }

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class SocialSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "name"]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(email=data["email"], password=data["password"])
        if not user:
            raise serializers.ValidationError("이메일 또는 비밀번호가 올바르지 않습니다.")
        return user
