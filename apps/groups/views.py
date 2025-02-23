from itertools import chain

from django.db.models import Count
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Group, GroupMember
from .serializers import GroupSerializer, GroupCreateSerializer, GroupMemberSerializer


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

        is_member = GroupMember.objects.filter(user=user, group=group).exists()
        """ 유저가 이 그룹에 가입했는지 확인 """
        is_admin = group.group_admin == user
        """ 유저가 그룹장인지 확인 """

        data = GroupSerializer(group).data
        data['is_member'] = is_member
        data['is_admin'] = is_admin
        return Response(data, status=status.HTTP_200_OK)

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