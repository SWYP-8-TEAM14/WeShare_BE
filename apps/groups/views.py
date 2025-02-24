from itertools import chain

from django.db.models import Count
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from .models import Group, GroupMember
from .serializers import GroupSerializer, GroupCreateSerializer, GroupMemberSerializer
from ..shared.models import Item
from ..shared.serializers import ItemSerializer


class GroupListView(generics.ListAPIView):
    """ 사용자가 가입한 그룹 목록 조회 """
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="created_by_me",
                type=str,
                description="내가 만든 그룹만 조회하려면 'true'로 설정",
                required=False
            )
        ]
    )
    def get_queryset(self):
        user = self.request.user
        joined_groups = Group.objects.filter(members__user=user).annotate(member_count=Count("members"))
        other_groups = Group.objects.exclude(group_id__in=joined_groups.values_list("group_id", flat=True)).annotate(
            member_count=Count("members"))

        queryset = list(chain(joined_groups, other_groups))
        return queryset


class GroupDetailView(generics.RetrieveAPIView):
    """ 특정 그룹 상세 조회(가입여부와 상관없이 접근 가능) """
    serializer_class = GroupCreateSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'group_id'

    def get(self, request, *args, **kwargs):
        group_id = kwargs.get('group_id')
        user = request.user

        try:
            group = Group.objects.annotate(member_count=Count("members")).get(group_id=group_id)
        except Group.DoesNotExist:
            return Response({"message" : "해당 그룹이 존재하지 않습니다."}, status=status.HTTP_404_NOT_FOUND)

        shared_items = list(Item.objects.filter(group=group))
        shared_items_data =  ItemSerializer(shared_items, many=True).data

        # 유저가 이 그룹에 가입했는지 확인
        is_member = GroupMember.objects.filter(user=user, group=group).exists()

        # 유저가 그룹장인지 확인
        is_admin = group.group_admin == user

        data = GroupSerializer(group).data
        data['is_member'] = is_member
        data['is_admin'] = is_admin
        data['shared_items'] = shared_items_data
        return Response(data, status=status.HTTP_200_OK)

class GroupManageView(APIView):
    """ 그룹 관리(그룹 상세 정보 + 그룹 정보 편집 가능 여부 포함) """
    permission_classes = [IsAuthenticated]

    def get(self, request, group_id):
        user = request.user

        try:
            group = Group.objects.annotate(member_count=Count("members")).get(group_id=group_id)
        except Group.DoesNotExist:
            return Response({"message" : "해당 그룹이 존재하지 않습니다."}, status=status.HTTP_404_NOT_FOUND)

        # 그룹장인지 확인(편집 권한 여부)
        is_admin = group.group_admin == user

        # 그룹 멤버 리스트 (4명까지만 표시)
        members = list(GroupMember.objects.filter(group=group)[:4])
        members_data = GroupMemberSerializer(members, many=True).data
        total_members = GroupMember.objects.filter(group=group).count()

        # 공용 물품 리스트 (5개 표시)
        shared_items = list(Item.objects.filter(group=group)[:5])
        shared_items_data = ItemSerializer(shared_items, many=True).data
        total_shared_items = Item.objects.filter(group=group).count()

        data = GroupSerializer(group).data
        data['is_admin'] = is_admin
        data['members'] = members_data
        data['total_members'] = total_members
        data['shared_items'] = shared_items_data
        data['total_shared_items'] = total_shared_items
        return Response(data, status=status.HTTP_200_OK)


class GroupMemberListView(APIView):
    """ 그룹 멤버 전체 리스트 조회 """
    permission_classes = [IsAuthenticated]

    def get(self, request, group_id):
        user = request.user

        try:
            group = Group.objects.get(group_id=group_id)
        except Group.DoesNotExist:
            return Response({"message" : "해당 그룹이 존재하지 않습니다."}, status=status.HTTP_404_NOT_FOUND)

        # 그룹 전체 멤버 리스트
        members = list(GroupMember.objects.filter(group=group))
        members_data = GroupMemberSerializer(members, many=True).data

        return Response({"members" :members_data}, status=status.HTTP_200_OK)


class GroupSharedItemListView(APIView):
    """ 특정 그룹 내 전체 공유 물품 리스트 조회 """
    permission_classes = [IsAuthenticated]

    def get(self, request, group_id):
        user = request.user

        try:
            group = Group.objects.get(group_id=group_id)
        except Group.DoesNotExist:
            return Response({"message" : "해당 그룹이 존재하지 않습니다."}, status=status.HTTP_404_NOT_FOUND)

        # 특정 그룹의 전체 공유 물품 리스트
        shared_items = list(Item.objects.filter(group=group))
        shared_items_data = ItemSerializer(shared_items, many=True).data

        return Response({"shared_items" : shared_items_data}, status=status.HTTP_200_OK)

class GroupCreateView(generics.CreateAPIView):
    """ 새로운 그룹 생성 """
    serializer_class = GroupCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        group = serializer.save(group_admin=self.request.user)
        GroupMember.objects.create(group=group, user=self.request.user, is_admin=True)


# class GroupJoinView(generics.RetrieveUpdateDestroyAPIView):
#     def create(self, request, *args, **kwargs):
#         group_id = self.kwargs.get('group_id')
#         user = request.user
#
#         if GroupMember.objects.filter(group_id=group_id, user=user).exists():
#             return Response({"message" : "이미 가입한 그룹입니다."}, status=status.HTTP_400_BAD_REQUEST)
#
#         GroupMember.objects.create(group_id=group_id, user=user)
#         return Response({"message" : "가입 신청 완료"}, status=status.HTTP_201_CREATED)


# class GroupLeaveView(generics.DestroyAPIView):
#     """ 그룹 탈퇴 """
#     permission_classes = [IsAuthenticated]
#
#     def delete(self, request, *args, **kwargs):
#         group_id = self.kwargs.get('group_id')
#         user = request.user
#
#         try:
#             group_member = GroupMember.objects.get(group_id=group_id, user=user)
#             group_member.delete()
#             return Response({"message" : "그룹 탈퇴 완료"}, status=status.HTTP_204_NO_CONTENT)
#         except GroupMember.DoesNotExist:
#             return Response({"message" : "가입되지 않은 그룹입니다."}, status=status.HTTP_404_NOT_FOUND)