"""
Base Permission
"""
from rest_framework import permissions


class IsPostOrIsAuthenticated(permissions.BasePermission):
    """
    Allowed Public POST for the register a user
    """

    def has_permission(self, request, view):
        """
        Check method
        """
        if request.method == 'POST':
            return True

        return request.user and request.user.is_authenticated


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Allowed Public POST, PUT, PATCH for admin only
    """

    def has_permission(self, request, view):
        """
        Check method POST, PUT & PATCH for admin only,
        and GET for everyone else.
        """
        if request.method in ['POST', 'PUT', 'PATCH']:
            if request.user.is_staff:
                return True
            else:
                return False

        return True
