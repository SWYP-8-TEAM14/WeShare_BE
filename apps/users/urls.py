from django.urls import path

from .views import LoginView, SignupView  # 필요에 따라 수정

urlpatterns = [
    path("signup/", SignupView.as_view(), name="signup"),
    path("login/", LoginView.as_view(), name="login"),
]
