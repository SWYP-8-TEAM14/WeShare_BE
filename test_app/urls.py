from django.urls import path
from .views import create_user_view, update_user_view, delete_user_view, get_user_view

urlpatterns = [
    path("create/", create_user_view, name="create_user"),                  # /users/create/?userid=1&username=JohnDoe
    path("update/<int:userid>/", update_user_view, name="update_user"),     # /users/update/1/?username=JaneDoe
    path("delete/<int:userid>/", delete_user_view, name="delete_user"),     # /users/delete/1/
    path("get/", get_user_view, name="get_all_users"),                      # /users/get/
    path("get/<int:userid>/", get_user_view, name="get_user"),              # /users/get/1/
]