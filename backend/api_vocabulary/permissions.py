# backend/api_vocabulary/permissions.py
from rest_framework.permissions import BasePermission

class IsAuthenticatedAndVerified(BasePermission):
    """
    Permiso personalizado que permite acceso solo a usuarios autenticados y con email verificado (is_active=True).
    """
    def has_permission(self, request, view):
        return bool(
            request.user and 
            request.user.is_authenticated and 
            request.user.is_active
        )