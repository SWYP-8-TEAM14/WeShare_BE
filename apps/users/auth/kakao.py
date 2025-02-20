import requests
from drf_spectacular.utils import extend_schema
from jsonschema.validators import extend
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from apps.users.models import User
from apps.users.serializers import KakaoLoginSerializer
from config.settings.base import env


class KakaoLoginView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(request=KakaoLoginSerializer, responses={200: "Success"})
    def get(self, request: Request) -> Response:
        kakao_auth_url = (
            f"https://kauth.kakao.com/oauth/authorize?"
            f"client_id={env("KAKAO_CLIENT_ID")}&"
            f"redirect_uri={env("KAKAO_REDIRECT_URI")}&"
            f"response_type=code"
        )
        return Response({"auth_url": kakao_auth_url}, status=status.HTTP_200_OK)


class KakaoCallbackView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        description="카카오 로그인 콜백 처리",
        responses={200: "사용자 정보 반환", 400: "Authorization code is missing"},
    )
    def get(self, request: Request) -> Response:
        code = request.query_params.get("code")
        if not code:
            return Response({"error": "Authorization code is missing"}, status=400)

        # Access Token 요청
        token_url = "https://kauth.kakao.com/oauth/token"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {
            "grant_type": "authorization_code",
            "client_id": env("KAKAO_CLIENT_ID"),
            "redirect_uri": env("KAKAO_REDIRECT_URI"),
            "code": code,
        }

        client_secret = env("KAKAO_SECRET", default=None)
        if client_secret:
            data["client_secret"] = client_secret

        token_response = requests.post(token_url, headers=headers, data=data)
        print("🔹 Token Response:", token_response.text)

        try:
            token_json = token_response.json()
            print("Token Response:", token_json)
        except requests.exceptions.JSONDecodeError:
            return Response(
                {"error": "Failed to prse JSON", "details": token_response.text},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        if token_response.status_code != 200:
            return Response(
                {"error": "Failed to get access token", "details": token_response.text},
                status=token_response.status_code,
            )

        access_token = token_response.json().get("access_token")
        print("🔹 Access Token:", access_token)

        # 사용자 정보 요청
        user_info_url = "https://kapi.kakao.com/v2/user/me"
        headers = {"Authorization": f"Bearer {access_token}"}
        user_info_response = requests.get(user_info_url, headers=headers)
        print("user Info response", user_info_response.json())

        if user_info_response.status_code != 200:
            return Response(
                {"error": "Failed to get user info", "details": user_info_response.text},
                status=user_info_response.status_code,
            )
        user_info = user_info_response.json()


        # 사용자 정보 추출
        kakao_account = user_info.get("kakao_account", {})
        profile = kakao_account.get("profile", {})
        email = kakao_account.get("email")
        username = profile.get("username")

        # 먼저 사용자를 조회합니다.
        existing_user = User.objects.filter(email=email).first()

        if existing_user:
            # 기존 사용자의 경우, 카카오 정보로 업데이트하지 않음
            user = existing_user
            created = False
        else:
            # 새로운 사용자 생성
            user = User.objects.create(
                email=email,
                username=profile.get("username", ""),
                is_active=True,
            )
            created = True

        refresh = RefreshToken.for_user(user)

        # 응답 반환
        return Response(
            {
                "access_token": str(refresh.access_token),
                "refresh_token": str(refresh),
                "message": "User information retrieved successfully",
                "user_id": user.id,
                "created": created,
                "user_data": {
                    "username": user.username,
                    "email": user.email,
                },
            },
            status=status.HTTP_200_OK,
        )
