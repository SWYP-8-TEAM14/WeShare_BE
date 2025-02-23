from typing import Any

from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from apps.users.models import User


class UserSerializer(ModelSerializer):  # type: ignore
    class Meta:
        model = User
        fields = ["id", "username", "email", "profile_image", "created_at", "updated_at"]
        read_only_fields = ["id", "email"]


class UserUpdateSerializer(serializers.ModelSerializer):  # type: ignore
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "profile_image",
            "created_at",
        ]
        read_only_fields = ["id", "email"]


def update(self: "UserSerializer", instance: User, validated_data: dict[str, Any]) -> User:
    # validated_data: 유효성 검사가 완료된 수정할 데이터
    # instance: 수정할 User 객체

    # 새로운 값이 있으면 업데이트, 없으면 기존 값 유지
    instance.username = validated_data.get("username", instance.username)
    instance.profile_image = validated_data.get("profile_image", instance.profile_image)

    instance.save()

    return instance


class SignupSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(required=False, allow_null=True)

    class Meta:
        model = User
        fields = ["email", "password", "username", "profile_image", "phone_number"]
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
        fields = ["email", "username"]

    def create(self, validated_data: dict[str, Any]) -> User:
        return User.objects.create_user(**validated_data)

class NaverLoginSerializer(serializers.ModelSerializer[User]):
    class Meta:
        model = User
        fields = ["email", "username"]

    def create(self, validated_data: dict[str, Any]) -> User:
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):  # type: ignore
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")

        user = authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError("유효하지 않은 자격 증명입니다.")
        return user
