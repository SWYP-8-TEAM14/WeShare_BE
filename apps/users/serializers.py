from typing import Any

from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import User


class UserSerializer(ModelSerializer):  # type: ignore
    class Meta:
        model = User
        fields = ["id", "nickname", "email", "profile_image", "social_type", "created_at", "updated_at"]
        read_only_fields = ["id", "email", "social_type"]


class UserUpdateSerializer(serializers.ModelSerializer):  # type: ignore
    class Meta:
        model = User
        fields = [
            "id",
            "nickname",
            "email",
            "profile_image",
            "social_type",
            "created_at",
        ]
        read_only_fields = ["id", "email", "social_type"]


def update(self: "UserSerializer", instance: User, validated_data: dict[str, Any]) -> User:
    # validated_data: 유효성 검사가 완료된 수정할 데이터
    # instance: 수정할 User 객체

    # 새로운 값이 있으면 업데이트, 없으면 기존 값 유지
    instance.nickname = validated_data.get("nickname", instance.nickname)
    instance.profile_image = validated_data.get("profile_image", instance.profile_image)

    instance.save()

    return instance


class SignupSerializer(serializers.ModelSerializer):  # type: ignore
    class Meta:
        model = User
        fields = ["email", "password", "username", "profile_image"]
        extra_kwargs = {
            "password": {"write_only": True},
            "profile_image": {"required": False},
        }

    def create(self, validated_data: dict[str, Any]) -> User:
        password = validated_data.get("password")
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user


class KakaoLoginSerializer(serializers.ModelSerializer[User]):
    class Meta:
        model = User
        fields = ["email", "nickname"]

    def create(self, validated_data: dict[str, Any]) -> User:
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):  # type: ignore
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data: dict[str, Any]) -> User:
        user = authenticate(email=data["email"], password=data["password"])
        if not isinstance(user, User):
            raise serializers.ValidationError("이메일 또는 비밀번호가 올바르지 않습니다.")
        return user
