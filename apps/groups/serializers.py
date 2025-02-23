from rest_framework import serializers
from apps.groups.models import Group, GroupMember


class GroupSerializer(serializers.ModelSerializer):
    member_count = serializers.IntegerField()

    class Meta:
        model = Group
        fields = ["group_id", "group_name", "group_image", "group_description", "member_count"]

        def get_member_count(self, obj):
            return GroupMember.objects.filter(group=obj).count()


class GroupCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ["group_name", "group_image", "group_description"]


class GroupMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupMember
        fields = "__all__"