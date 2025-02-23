from datetime import timedelta

import requests
from django.contrib.auth import authenticate
from drf_spectacular.utils import extend_schema, OpenApiExample
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.users import serializers
from apps.users.models import User
from apps.users.serializers import (
    LoginSerializer,
    SignupSerializer,
    UserUpdateSerializer,
)
from config.settings.base import env


class HomeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request) -> Response:
        return Response(
            {
                "message": "WeShare 홈 접속 성공",
            }
        )


class SignupView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(request=SignupSerializer, responses={201: "회원가입 성공"})
    def post(self, request: Request) -> Response:
        data = request.data.copy()

        if not data.get("phone_number"):
            data["phone_number"] = None

        serializer = SignupSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "회원가입 성공"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

    @extend_schema(
        tags=["user"],
        summary="User Login",
        description="Login with email and password to get access and refresh tokens",
        request=LoginSerializer,
        examples=[
            OpenApiExample(
                "Login Example",
                value={"email": "user@example.com", "password": "string"},
                request_only=True,
            )
        ],
        responses={
            200: {
                "type": "object",
                "properties": {
                    "message": {"type": "string"},
                    "access_token": {"type": "string"},
                    "refresh_token": {"type": "string"},
                    "user_id": {"type": "integer"},
                },
            }
        },
    )
    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        # `authenticate`에서 `email`을 사용하여 사용자 검증
        user = authenticate(email=email, password=password)

        if not user:
            raise serializers.ValidationError("유효하지 않은 자격 증명입니다.")

        # JWT 토큰 생성 (super() 호출)
        data = super().validate(attrs)
        data["message"] = "로그인 성공"
        data["user_id"] = user.id

        return data

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["email"] = user.email  # 추가 정보 포함 가능


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request: Request) -> Response:
        try:
            refresh_token = request.data.get("refresh_token")
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
            return Response({"message": "로그아웃 성공"}, status=status.HTTP_200_OK)

        except Exception:
            return Response({"message": "로그아웃 처리 중 에러 발생"}, status=status.HTTP_400_BAD_REQUEST)


class UserUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request: Request) -> Response:
        try:
            user = User.objects.get(id=request.user.id)
            serializer = UserUpdateSerializer(user, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(
                    {"message": "회원 정보 수정 성공"},
                    status=status.HTTP_200_OK,
                )

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except User.DoesNotExist:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)


class UserDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request: Request) -> Response:
        try:
            user = User.objects.get(id=request.user.id)
            user.delete()
            return Response({"message": "회원 탈퇴 성공"}, status=status.HTTP_204_NO_CONTENT)

        except User.DoesNotExist:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)


class KakaoReissueView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request: Request) -> Response:
        refresh_token = request.data.get("refresh_token")

        if not refresh_token:
            return Response({"error": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)

        token_url = "https://kauth.kakao.com/oauth/token"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {
            "grant_type": "refresh_token",
            "client_id": env("KAKAO_CLIENT_ID"),
            "refresh_token": refresh_token,
        }

        try:
            response = requests.post(token_url, headers=headers, data=data)
            response.raise_for_status()
            return Response(response.json(), status=status.HTTP_200_OK)

        except requests.RequestException as e:
            return Response({"error": "Failed to reissue token", "details": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class NaverReissueView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request: Request) -> Response:
        refresh_token = request.data.get("refresh_token")

        if not refresh_token:
            return Response({"error": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)

        token_url = "https://nid.naver.com/oauth2.0/token"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {
            "grant_type": "refresh_token",
            "client_id": env("NAVER_CLIENT_ID"),
            "client_secret": env("NAVER_CLIENT_SECRET"),
            "refresh_token": refresh_token,
        }

        try:
            response = requests.post(token_url, headers=headers, data=data)
            response.raise_for_status()
            return Response(response.json(), status=status.HTTP_200_OK)

        except requests.RequestException as e:
            return Response({"error": "Failed to reissue token", "details": str(e)}, status=status.HTTP_400_BAD_REQUEST)
