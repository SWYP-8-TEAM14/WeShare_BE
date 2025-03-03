import requests
import logging
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from apps.users.models import User
from apps.users.serializers import KakaoLoginSerializer
from config.settings.base import env

from django.http import JsonResponse, HttpResponseRedirect
import os

class KakaoLoginView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(request=KakaoLoginSerializer, responses={200: "Success"})
    def get(self, request: Request) -> Response:
        kakao_auth_url = (
            f"https://kauth.kakao.com/oauth/authorize?"
            f"client_id={env('KAKAO_CLIENT_ID')}&"
            f"redirect_uri={env('KAKAO_REDIRECT_URI')}&"
            f"response_type=code"
        )
        return Response({"auth_url": kakao_auth_url}, status=status.HTTP_200_OK)


@method_decorator(csrf_exempt, name="dispatch")
class KakaoCallbackView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        description="카카오 로그인 콜백 처리",
        responses={200: "사용자 정보 반환", 400: "Authorization code is missing"},
    )
    def get(self, request: Request) -> Response:
        code = request.query_params.get("code")
        if not code:
            return Response({"error" : "Authorization code is missing"}, status=status.HTTP_400_BAD_REQUEST)
        return self.process_code(code)

    def post(self, request: Request) -> Response:
        code = request.data.get("code") or request.query_params.get("code")
        if not code:
            return Response({"error": "Authorization code is missing"}, status=400)
        return self.process_code(code)

    def process_code(self, code):
        # Access Token 요청
        token_url = "https://kauth.kakao.com/oauth/token"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {
            "grant_type": "authorization_code",
            "client_id": env("KAKAO_CLIENT_ID"),
            "client_secret": env("KAKAO_SECRET"),
            "redirect_uri": env("KAKAO_REDIRECT_URI"),
            "code": code,
        }

        token_response = requests.post(token_url, headers=headers, data=data)
        if token_response.status_code != 200:
            return Response(
                {"error": "Failed to get access token", "details": token_response.text},
                status=token_response.status_code,
            )

        try:
            token_json = token_response.json()
            access_token = token_json.get("access_token")
        except requests.exceptions.JSONDecodeError:
            return Response(
                {"error": "Failed to parse JSON", "details": token_response.text},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        if not access_token:
            return Response(
                {"error": "Failed to get access token", "details": token_json},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        # 사용자 정보 요청
        user_info_url = "https://kapi.kakao.com/v2/user/me"
        headers = {"Authorization": f"Bearer {access_token}"}
        user_info_response = requests.get(user_info_url, headers=headers)

        if user_info_response.status_code != 200:
            return Response(
                {"error": "Failed to get user info", "details": user_info_response.text},
                status=user_info_response.status_code,
            )
        user_info = user_info_response.json()

        # 사용자 정보 추출
        kakao_id = user_info.get("id")  # 카카오 고유 ID
        kakao_account = user_info.get("kakao_account", {})
        profile = kakao_account.get("profile", {})
        email = kakao_account.get("email")
        nickname = profile.get("nickname")  # username이 아니라 nickname!

        # 이메일이 없는 경우 기본 이메일 생성
        if not email:
            email = f"kakao_{kakao_id}@example.com"

        # 기존 사용자인지 확인 (kakao_id 기반 조회)
        user = User.objects.filter(kakao_id=kakao_id).first()

        if user:
            # 기존 유저 → 로그인 처리
            created = False
        else:
            # 신규 가입
            user = User.objects.create(
                kakao_id=kakao_id,
                email=email,
                username=nickname,
                is_active=True,
            )
            created = True

        # JWT 토큰 생성
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        response = HttpResponseRedirect(os.getenv("FRONTEND_REDIRECT_URI"))
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=False,
            samesite="Lax",
        )
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=False,
            samesite="Lax",
        )

        return response
