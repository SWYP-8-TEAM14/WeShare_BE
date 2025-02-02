from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(BaseModel):
    provider_id = models.CharField(max_length=255, null=True, blank=True, unique=True)
    provider = models.CharField(max_length=20, null=True, blank=True)
    group_admin_id = models.IntegerField(null=True, blank=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=100, unique=True)
    nickname = models.CharField(max_length=20)
    profile_image = models.CharField(max_length=255, null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "users"
        verbose_name = "유저"
        verbose_name_plural = "유저정보"

    def __str__(self):
        return self.nickname