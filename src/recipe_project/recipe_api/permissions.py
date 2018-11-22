from rest_framework import permissions
from . import views

class IsOwner(permissions.BasePermission):
    """This is the base permission class for all the requests so that they are authenticated"""
    def has_permission(self, request, view):
        if isinstance(view,views.UserProfileViewSet) and request.method == "POST":
            return True
        elif request.auth is not None:
            return True
        return False

class UpdateOwnProfile(permissions.BasePermission):
    """Allow users to edit their own profiles"""

    def has_object_permission(self, request, view, obj):
        """Check user is trying to edit their own profiles"""

        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.id == request.user.id

class UpdateOwnRecipe(permissions.BasePermission):
    """Allows users to update their recipies"""

    def has_object_permission(self, request, view, obj):
        """Check if the user is trying to edit their own recipies"""

        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.created_by == request.user
