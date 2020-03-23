from rest_framework import permissions


class UpdateOwnProfile(permissions.BasePermission):
    """Allow user to edit their own profile"""

    def has_object_permission(self, request, view, obj):
        """Check user is trying to edit their own profile"""
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.id == request.user.id


class IsServiceProvider(permissions.BasePermission):
    """
    Allows access only to Service Provider.
    """

    def has_permission(self, request, view):
        if request.user.user_type == 'Service Provider':
            return True


class IsConsumer(permissions.BasePermission):
    """
    Allows access only to Consumer.
    """

    def has_permission(self, request, view):
        if request.user.user_type == 'Consumer':
            return True

