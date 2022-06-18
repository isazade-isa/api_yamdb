from rest_framework import permissions


class IsAuthorOrModeratorPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return (
            obj.author == request.user
            or request.method in permissions.SAFE_METHODS
            or ((request.user.is_moderator or request.user.is_admin)
                and request.user.is_authenticated)
        )


class IsAuthorOrStaffOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif request.user.is_anonymous:
            return False
        else:
            return (request.user.is_admin
                    or request.user.is_moderator
                    or obj.author == request.user)
