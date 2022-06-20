from rest_framework import permissions


class IsAuthorOrStaffOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif request.user.USER:
            return False
        else:
            return (request.user.ADMIN
                    or request.user.MODERATOR
                    or obj.author == request.user)
