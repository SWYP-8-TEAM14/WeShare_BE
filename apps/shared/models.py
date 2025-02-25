from django.db import models

from apps.groups.models import Group
from apps.users.models import User
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin


# test code
class User(AbstractUser, PermissionsMixin):
    kakao_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    group_admin_id = models.IntegerField(null=True, blank=True)
    phone_number = models.CharField(max_length=100, unique=True, null=True, blank=True)
    username = models.CharField(max_length=20, unique=True)
    profile_image = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    groups = models.ManyToManyField(
        "auth.Group",
        related_name="shared_custom_user_groups",
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="shared_custom_user_permissions",
        blank=True,
    )

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    class Meta:
        db_table = "shared_users"
        verbose_name = "유저"
        verbose_name_plural = "유저정보"

    def __str__(self) -> str:
        return self.username



# -------------------------------------------------------------
class Item(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='items')
    item_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # group_id = models.ForeignKey(Group, on_delete=models.CASCADE)
    # group_id = models.IntegerField()
    item_name = models.CharField(max_length=255)
    item_description = models.TextField(null=True, blank=True)
    item_image = models.TextField(null=True, blank=True)
    status = models.IntegerField(default=1)  # 1: 사용 가능, 0: 대여 중
    quantity = models.IntegerField(default=1)
    caution = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)


class Reservation(models.Model):
    reservation_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    reservation_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=50)  # '예약 완료', '취소됨' 등
    created_at = models.DateTimeField(null=True, blank=True)

class RentalRequest(models.Model):
    request_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    requested_at = models.DateTimeField(null=True, blank=True)


class RentalRecord(models.Model):
    rental_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    rental_start = models.DateTimeField()
    rental_end = models.DateTimeField()
    actual_return = models.DateTimeField(null=True, blank=True)
    rental_status = models.CharField(max_length=50)  # '대여 중', '반납 완료'
    created_at = models.DateTimeField(null=True, blank=True)
