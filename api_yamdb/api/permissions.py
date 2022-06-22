from rest_framework import permissions
from users.models import CustomUser

# class IsAuthorOrModeratorPermission(permissions.BasePermission):

#     def has_object_permission(self, request, view, obj):
#         return (
#             obj.author == request.user
#             or request.method in permissions.SAFE_METHODS
#             or ((request.user.is_moderator or request.user.is_admin)
#                 and request.user.is_authenticated)
#         )


# class IsAuthorOrStaffOrReadOnly(permissions.BasePermission):
#
#     def has_object_permission(self, request, view, obj):
#         if request.method in permissions.SAFE_METHODS:
#             return True
#         elif request.user.is_anonymous:
#             return False
#         else:
#             return (request.user.is_admin
#                     or request.user.is_moderator
#                     or obj.author == request.user)

class IsAuthorOrStaffOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return bool(request.user.is_staff or request.user.role == 'admin')


class IsUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.user.role in CustomUser.USER:
                return True
        return False


class IsModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.user.role in CustomUser.MODERATOR:
                return True
        return False


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.user.role in CustomUser.ADMIN:
                return True
            return False


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return obj.author == request.user
        else:
            return False


class IsTest(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif request.user.is_anonymous:
            return False
        else:
            return (request.user.is_admin
                    or request.user.is_moderator
                    or obj.author == request.user)
