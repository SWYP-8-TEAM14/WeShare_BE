from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()


class Group(models.Model):
    group_id = models.AutoField(primary_key=True)
    group_admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name="admin_group")
    group_name = models.CharField(max_length=120)
    group_image = models.CharField(max_length=255, null=True, blank=True)
    group_description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.group_name


class GroupMember(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="members")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_groups")
    is_admin = models.BooleanField(default=False)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("group", "user")

    def __str__(self):
        return f"{self.user.username} - {self.group}"