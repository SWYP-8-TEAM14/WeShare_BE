from typing import Any

import requests
from django.http import HttpRequest, HttpResponse
from django.utils.crypto import get_random_string
from django.views.generic import RedirectView
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from apps.users.models import User
from config.settings.base import env

# from typing import Any, cast
# from django.conf import settings
# from django.http import HttpRequest

NAVER_CALLBACK_URL = "/auth/naver/callback/"
NAVER_STATE = "naver_login"
NAVER_LOGIN_URL = "https://nid.naver.com/oauth2.0/authorize"


class NaverLoginView(RedirectView):
    permission_classes = [AllowAny]

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        state = get_random_string(32)
        naver_login_url = (
            f"https://nid.naver.com/oauth2.0/authorize?"
            f"response_type=code&client_id={env('NAVER_CLIENT_ID')}"
            f"&redirect_uri={env('NAVER_REDIRECT_URI')}&state={state}"
        )
        return Response({"naver_login_url": naver_login_url}, status=status.HTTP_200_OK)


class NaverCallbackView(APIView):
    permission_classes = [AllowAny]

    def get(self, request: Request) -> Response:
        # 콜백으로 전달된 code와 state 파라미터 받기
        code = request.GET.get("code")

        if not code:
            return Response({"error": "Authorization code is missing"}, status=400)
        state = request.GET.get("state")
        print(f"🔹 Received State: '{state}'")

        # 액세스 토큰 요청
        token_url = (
            f"https://nid.naver.com/oauth2.0/token?"
            f"grant_type=authorization_code&client_id={env("NAVER_CLIENT_ID")}"
            f"&client_secret={env("NAVER_SECRET")}&code={code}&state={state}"
        )
        token_response = requests.get(token_url)
        token_data = token_response.json()

        if "access_token" not in token_data:
            return Response({"error": "Failed to retrieve access token"}, status=status.HTTP_400_BAD_REQUEST)

        access_token = token_data["access_token"]

        # 사용자 정보 요청
        profile_url = "https://openapi.naver.com/v1/nid/me"
        headers = {"Authorization": f"Bearer {access_token}"}
        profile_response = requests.get(profile_url, headers=headers)
        profile_data = profile_response.json()

        if profile_data.get("message") != "success":
            return Response({"error": "Failed to retrieve user profile"}, status=status.HTTP_400_BAD_REQUEST)

        # 사용자 정보 추출
        user_info = profile_data["response"]
        email = user_info.get("email")

        # 기존 사용자 조회
        existing_user = User.objects.filter(email=email).first()

        if existing_user:
            # 기존 사용자의 경우, 네이버 정보로 업데이트하지 않음
            user = existing_user
            created = False
        else:
            # 새로운 사용자 생성
            user = User.objects.create(
                email=email,
                username=user_info.get("username", ""),
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
                    "email": user.email,
                    "username": user.username,
                },
            },
            status=status.HTTP_200_OK,
        )
