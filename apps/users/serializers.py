from rest_framework import serializers

from .models import User


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
        fields = ["email", "name"]
