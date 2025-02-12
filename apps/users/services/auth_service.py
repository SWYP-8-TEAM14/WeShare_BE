from django.contrib.auth import authenticate

from apps.users.models import User


class AuthService:
    @staticmethod
    def authenticate_user(email, password):
        user = authenticate(email=email, password=password)
        if user and user.is_active:
            return user
        return None
