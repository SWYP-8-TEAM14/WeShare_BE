from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Group, GroupMember
from .serializers import GroupSerializer, GroupCreateSerializer, GroupMemberSerializer


class GroupListView(generics.ListAPIView):
    """ 사용자가 가입한 그룹 목록 조회 """
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Group.objects.filter(members__user=self.request.user)
        if self.request.GET.get("created_by_me") == "true":
            queryset = queryset.filter(group_admin=self.request.user)
        return queryset


class GroupDetailView(generics.RetrieveAPIView):
    """ 특정 그룹 상세 조회 """
    serializer_class = GroupCreateSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'group_id'

    def get_queryset(self):
        return Group.objects.all()


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