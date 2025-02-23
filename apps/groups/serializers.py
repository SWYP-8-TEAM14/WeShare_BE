from rest_framework import serializers
from .models import Group, GroupMember


class GroupSerializer(serializers.ModelSerializer):
    member_count = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = ["group_id", "group_name", "group_image", "member_count"]

        def get_member_count(self, obj):
            return obj.members.count()


class GroupCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ["group_name", "group_image", "group_description"]


class GroupMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupMember
        fields = "__all__"