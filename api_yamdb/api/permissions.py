from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """Checking the access group for the Admin and other users."""

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_authenticated
                    and request.user.is_admin))

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_authenticated
                    and request.user.is_admin))


class AuthorAdminModeratorOrReadOnly(permissions.BasePermission):
    """Checking the access group for the AuthorAdminModerator."""

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return ((request.method in permissions.SAFE_METHODS)
                or (obj.author == request.user
                or request.user.is_moderator
                or request.user.is_admin))


class IsAdminOnly(permissions.BasePermission):
    """Checking the access group for the Admin."""

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.is_admin
        )
