import random
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.groups.models import Group, GroupMember

User = get_user_model()

class Command(BaseCommand):
    help = "Create dummy data for users and groups"

    def handle(self, *args, **kwargs):
        # 슈퍼유저 생성 (최소 1명 필요)
        admin_email = "admin@example.com"
        if not User.objects.filter(email=admin_email).exists():
            admin_user = User.objects.create_superuser(
                email=admin_email,
                username="admin",
                password="admin1234"
            )
            self.stdout.write(self.style.SUCCESS(f"Superuser '{admin_user.email}' created."))
        else:
            admin_user = User.objects.get(email=admin_email)

        # 그룹 생성 (기존에 없을 경우)
        group_names = ["테니스 모임", "마포 스크린골프", "도보마포"]
        groups = {}
        for name in group_names:
            group, created = Group.objects.get_or_create(
                group_name=name,
                defaults={
                    "group_description": f"{name}에 오신 것을 환영합니다!",
                    "group_admin": admin_user  # 관리자 지정
                }
            )
            groups[name] = group
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created group: {name} (Admin: {admin_user.email})"))

        # 일반 유저 생성 (10명)
        for i in range(10):
            email = f"user{i+1}@example.com"
            username = f"user{i+1}"

            if not User.objects.filter(email=email).exists():
                user = User.objects.create_user(
                    email=email,
                    username=username,
                    password="password1234",
                )

                # 랜덤 그룹에 배정
                assigned_group = random.choice(list(groups.values()))
                GroupMember.objects.create(user=user, group=assigned_group)

                self.stdout.write(
                    self.style.SUCCESS(
                        f"Created user: {username} (Group: {assigned_group.group_name})"
                    )
                )

        self.stdout.write(self.style.SUCCESS("Dummy data creation completed!"))
