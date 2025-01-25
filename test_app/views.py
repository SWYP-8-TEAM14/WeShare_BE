from django.http import JsonResponse
from .service import add_user, update_user, delete_user

from django.http import JsonResponse
from .models import User
from django.core.exceptions import ObjectDoesNotExist

def get_user_view(request, userid=None):
    """
    Retrieve a specific user or all users.
    Example:
    - Retrieve all users: /users/get/
    - Retrieve a specific user: /users/get/1/
    """
    if request.method == "GET":
        if userid:
            # 특정 사용자 조회
            try:
                user = User.objects.get(userid=userid)
                return JsonResponse({
                    "status": "success",
                    "user": {
                        "userid": user.userid,
                        "username": user.username
                    }
                })
            except ObjectDoesNotExist:
                return JsonResponse({"status": "error", "message": "User not found"}, status=404)
        else:
            # 모든 사용자 조회
            users = User.objects.all().values("userid", "username")
            return JsonResponse({
                "status": "success",
                "users": list(users)
            })
    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)

def create_user_view(request):
    """
    Create a new user via GET request.
    Example: /users/create/?userid=1&username=JohnDoe
    """
    if request.method == "GET":
        userid = request.GET.get("userid")
        username = request.GET.get("username")
        if userid and username:
            user = add_user(userid=userid, username=username)
            return JsonResponse({"status": "success", "userid": user.userid, "username": user.username})
        return JsonResponse({"status": "error", "message": "Missing userid or username"}, status=400)
    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)

def update_user_view(request, userid):
    """
    Update an existing user's username via GET request.
    Example: /users/update/1/?username=JaneDoe
    """
    if request.method == "GET":
        new_username = request.GET.get("username")
        if new_username:
            user = update_user(userid=userid, new_username=new_username)
            if user:
                return JsonResponse({"status": "success", "userid": user.userid, "username": user.username})
            return JsonResponse({"status": "error", "message": "User not found"}, status=404)
        return JsonResponse({"status": "error", "message": "Missing username"}, status=400)
    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)

def delete_user_view(request, userid):
    """
    Delete an existing user via GET request.
    Example: /users/delete/1/
    """
    if request.method == "GET":
        success = delete_user(userid=userid)
        if success:
            return JsonResponse({"status": "success", "message": "User deleted"})
        return JsonResponse({"status": "error", "message": "User not found"}, status=404)
    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)