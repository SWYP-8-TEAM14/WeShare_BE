from django.urls import path

# from .auth.kakao import KakaoCallbackView, KakaoLoginView
from .auth.naver import NaverCallbackView, NaverLoginView
from .auth.views import LoginView, SignupView
from .views import UserView

urlpatterns = [
    path("signup/", SignupView.as_view(), name="signup"),
    path("login/", LoginView.as_view(), name="login"),
]
