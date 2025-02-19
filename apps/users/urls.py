from django.urls import path

from .auth.kakao import KakaoCallbackView, KakaoLoginView
from .auth.naver import NaverCallbackView, NaverLoginView
from .auth.views import (
    KakaoReissueView,
    LogoutView,
    NaverReissueView,
    SignupView,
    UserDeleteView,
    UserUpdateView,
)
from .views import UserView

urlpatterns = [
    path("api/v1/user/", UserView.as_view()),
    path("api/v1/signup/", SignupView.as_view(), name="signup"),
    path("api/v1/user/patch/", UserUpdateView.as_view(), name="user-update"),
    path("api/v1/user/delete/", UserDeleteView.as_view(), name="user-delete"),
    path("api/v1/user/logout/", LogoutView.as_view(), name="logout"),
    path("api/v1/user/auth/kakao/", KakaoLoginView.as_view(), name="kakao-login"),
    path("api/v1/user/auth/kakao/callback/", KakaoCallbackView.as_view(), name="kakao-callback"),
    path("api/v1/user/auth/naver/", NaverLoginView.as_view(), name="naver-login"),
    path("api/v1/user/auth/naver/callback/", NaverCallbackView.as_view(), name="naver-callback"),
    path("api/v1/user/auth/kakao/reissue/", KakaoReissueView.as_view(), name="kakao-reissue"),
    path("api/v1/user/auth/naver/reissue/", NaverReissueView.as_view(), name="naver-reissue"),
]
