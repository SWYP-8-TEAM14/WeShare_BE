from django.urls import path

from .auth.kakao import KakaoCallbackView, KakaoLoginView
from .auth.naver import NaverCallbackView, NaverLoginView
from .auth.views import (
    HomeView,
    KakaoReissueView,
    LoginView,
    LogoutView,
    NaverReissueView,
    SignupView,
    UserDeleteView,
    UserUpdateView,
)
from .views import UserView

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("login/", LoginView.as_view()),
    path("signup/", SignupView.as_view(), name="signup"),
    path("patch/", UserUpdateView.as_view(), name="user-update"),
    path("delete/", UserDeleteView.as_view(), name="user-delete"),
    path("logout/", LogoutView.as_view(), name="logout"),

    # 소셜로그인
    path("user/auth/kakao/login/", KakaoLoginView.as_view(), name="kakao-login"),
    path("user/auth/kakao/login/callback/", KakaoCallbackView.as_view(), name="kakao-callback"),
    path("user/auth/naver/login/", NaverLoginView.as_view(), name="naver-login"),
    path("user/auth/naver/login/callback/", NaverCallbackView.as_view(), name="naver-callback"),
    path("user/auth/kakao/reissue/", KakaoReissueView.as_view(), name="kakao-reissue"),
    path("user/auth/naver/reissue/", NaverReissueView.as_view(), name="naver-reissue"),
]
