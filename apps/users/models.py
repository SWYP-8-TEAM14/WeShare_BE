from typing import TYPE_CHECKING, Any, Optional, TypeVar, cast

from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.db import models

UserType = TypeVar("UserType", bound="User")


class UserManager(BaseUserManager[UserType]):
    def create_user(
        self, email: str, username: str, password: Optional[str] = None, **extra_fields: dict[str, Any]
    ) -> UserType:
        if not email:
            raise ValueError("이메일은 필수입니다.")
        if not username:
            raise ValueError("닉네임(username)은 필수입니다.")

        extra_fields.pop("username", None)

        user: UserType = self.model(email=self.normalize_email(email), username=username, **extra_fields)
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email: str, password: Optional[str] = None, **extra_fields: dict[str, Any]) -> "User":
        extra_fields.setdefault("is_staff", cast(Any, True))
        extra_fields.setdefault("is_superuser", cast(Any, True))

        return self.create_user(email, password, **extra_fields)


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(BaseModel, AbstractUser, PermissionsMixin):
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    SOCIAL_CHOICES = [("KAKAO", "Kakao"), ("NAVER", "Naver")]

    kakao_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    group_admin_id = models.IntegerField(null=True, blank=True)
    phone_number = models.CharField(max_length=100, unique=True, null=True, blank=True)
    username = models.CharField(max_length=20, unique=True)
    profile_image = models.CharField(max_length=255, null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    groups = models.ManyToManyField(
        "auth.Group",
        related_name="custom_user_groups",
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="custom_user_permissions",
        blank=True,
    )

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    class Meta:
        db_table = "users"
        verbose_name = "유저"
        verbose_name_plural = "유저정보"

    def __str__(self) -> str:
        return self.username
