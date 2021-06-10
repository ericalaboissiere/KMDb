from rest_framework.permissions import BasePermission


class AdminPermission(BasePermission):
    def has_permission(self, request, view):

        if request.method == 'POST' and request.user.is_superuser and request.user.is_staff:
            return True

        if request.method == 'DELETE' and request.user.is_superuser and request.user.is_staff:
            return True

        if request.method == 'GET':
            return True

        return False


class CriticPermission(BasePermission):
    def has_permission(self, request, view):

        if request.method == 'POST' and request.user.is_superuser == False and request.user.is_staff:
            return True

        if request.method == 'PUT' and request.user.is_superuser == False and request.user.is_staff:
            return True

        return False


class UserPermission(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_staff == False
            and request.user.is_superuser == False
        )
