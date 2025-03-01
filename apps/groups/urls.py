from django.urls import path
from .views import (
    GroupListView, GroupDetailView, GroupCreateView, GroupManageView, GroupMemberListView, GroupSharedItemListView
)


urlpatterns = [
    path("groups/", GroupListView.as_view(), name="group-list"),
    path("groups/<int:group_id>/", GroupDetailView.as_view(), name="group-detail"),
    path("groups/<int:group_id>/manage/", GroupManageView.as_view(), name="group-manage"),
    path("groups/<int:group_id>/manage/members/", GroupMemberListView.as_view(), name="group-member-list"),
    path("groups/<int:group_id>/items/", GroupSharedItemListView.as_view(), name="group-shared-item-list"),
    path("groups/create/", GroupCreateView.as_view(), name="group-create"),
]