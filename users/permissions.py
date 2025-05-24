from rest_framework import permissions


class IsUser(permissions.BasePermission):
    """Проверка пользователя на статус владельца объекта."""
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
