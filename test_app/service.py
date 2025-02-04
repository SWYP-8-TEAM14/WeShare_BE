from .models import User


def add_user(userid, username):
    """
    Adds a new user to the database.
    """
    user = User.objects.create(userid=userid, username=username)
    return user


def update_user(userid, new_username):
    """
    Updates the username for a given user.
    """
    try:
        user = User.objects.get(userid=userid)
        user.username = new_username
        user.save()
        return user
    except User.DoesNotExist:
        return None


def delete_user(userid):
    """
    Deletes a user from the database by userid.
    """
    try:
        user = User.objects.get(userid=userid)
        user.delete()
        return True
    except User.DoesNotExist:
        return False
