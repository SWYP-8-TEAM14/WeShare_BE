from typing import Optional

from django.contrib.auth import authenticate

from apps.users.models import User


class AuthService:
    @staticmethod
    def authenticate_user(email: str, password: str) -> Optional[User]:
        user = authenticate(email=email, password=password)
        if isinstance(user, User) and user.is_active:
            return user
        return None
