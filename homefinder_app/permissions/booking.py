from rest_framework import permissions

from homefinder_app.enums import Role


class BookingPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.user.role == Role.admin.name:
            return True
        if request.method in permissions.SAFE_METHODS:
            return True
        if view.action == 'create' and request.user.role == Role.tenant.name:
            return True
        return False


    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.user.role == Role.admin.name:
            return True
        if request.method in permissions.SAFE_METHODS:
            return obj.guest == request.user or obj.housing.owner == request.user
        if view.action == 'cancel' and obj.guest == request.user:
            return True
        if view.action in ['approve', 'reject'] and obj.housing.owner == request.user:
            return True

        return False



class BookingActionPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        user = request.user

        if user.role == Role.admin.name:
            return True

        if view.action == 'cancel':
            return obj.guest == user

        if view.action in ('approve', 'reject'):
            return obj.housing.owner == user

        return False
