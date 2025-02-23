from django.urls import path
from .views import (
    GroupListView, GroupDetailView, GroupCreateView
)


urlpatterns = [
    path("groups/", GroupListView.as_view(), name="group-list"),
    path("groups/<int:group_id>/", GroupDetailView.as_view(), name="group-detail"),
    path("groups/create/", GroupCreateView.as_view(), name="group-create"),
]