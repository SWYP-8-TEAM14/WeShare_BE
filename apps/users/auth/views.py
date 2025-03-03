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

from apps.groups.models import GroupMember
# from apps.shared.models import Item
from apps.users import serializers
from apps.users.models import User
from apps.users.serializers import (
    LoginSerializer,
    SignupSerializer,
    UserUpdateSerializer,
)
from config.settings.base import env


class HomeView(APIView):
    """ WeShare 홈 화면 API """
    permission_classes = [AllowAny]

    def get(self, request: Request) -> Response:
        user = request.user

        # 가입된 그룹 ID 목록 가져오기
        joined_groups = GroupMember.objects.filter(user=user).values_list("group_id", flat=True)

        available_items = (
            Item.objects.filter(group_id__in=joined_groups, status=1)
            .order_by("-created_at")[:4]
        )
        available_items_data = [{"id": item.id, "name": item.item_name, "group": item.group.group_name} for item in available_items]

        response_data = {
            "message": "WeShare 홈 접속 성공",
            "buttons": {
                "reservation": "/api/v1/shared/items/reservations/",
                "pickup": "/api/v1/shared/items/pickup/",
                "return": "/api/v1/shared/items/return/",
            },
            "available_items": available_items_data,
            "tabs": ["홈", "내 그룹", "공유물품", "마이페이지"],
        }

        return Response(response_data, status=200)


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
            user = request.user
            serializer = UserUpdateSerializer(user, data=request.data, partial=True)

            if serializer.is_valid():
                validated_data = serializer.validated_data
                allowed_fields = ["profile_image", "username"]
                update_data = {k: v for k,v in validated_data.items() if k in allowed_fields}
                serializer.save(**update_data)
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
