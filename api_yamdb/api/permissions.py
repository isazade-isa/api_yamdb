from rest_framework import permissions


class IsAuthorOrModeratorPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return (
            obj.author == request.user
            or request.method in permissions.SAFE_METHODS
            or ((request.user.is_moderator or request.user.is_admin)
                and request.user.is_authenticated)
        )
