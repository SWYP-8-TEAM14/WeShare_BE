from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from .models import User


class UserSerializer(ModelSerializer["User"]):
    class Meta:
        model = User
        fields = ["id", "nickname", "email", "profile_image", "created_at", "updated_at"]


class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "password", "nickname", "profile_image"]
        extra_kwargs = {
            "password": {"write_only": True},


class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "nickname", "password", "name"]
        extra_kwargs = {
            "profile_image": {"required": False},
        }

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class SocialSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "nickname"]

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
        fields = ["email", "name"]
