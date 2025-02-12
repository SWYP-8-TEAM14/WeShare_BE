from typing import Optional

from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.db.models import CharField, DateTimeField, IntegerField


class UserManager(BaseUserManager["User"]):
    def create_user(self, email, password: Optional[str] = None, **extra_fields: dict) -> "User":
        if not email:
            raise ValueError("이메일은 필수입니다.")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)


class BaseModel(models.Model):
    created_at: DateTimeField = models.DateTimeField(auto_now_add=True)
    updated_at: DateTimeField = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(BaseModel, AbstractUser, PermissionsMixin):
    provider_id: CharField = models.CharField(max_length=255, null=True, blank=True, unique=True)
    provider = models.CharField(max_length=20, null=True, blank=True)
    group_admin_id = models.IntegerField(null=True, blank=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=100, unique=True)
    nickname = models.CharField(max_length=20, unique=True)
    profile_image = models.CharField(max_length=255, null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager["User"] = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        db_table = "users"
        verbose_name = "유저"
        verbose_name_plural = "유저정보"

    def __str__(self):
        return self.nickname
