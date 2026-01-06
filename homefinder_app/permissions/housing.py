from rest_framework import permissions

from homefinder_app.enums import Role


# class HousingPermission(permissions.BasePermission):
#     def has_permission(self, request, view):
#         if request.user.role == Role.admin.name:
#             return True
#         if request.method in permissions.SAFE_METHODS:
#             return True
#         return request.user.role == Role.owner.name
#
#
#     def has_object_permission(self, request, view, obj):
#         if request.user.role == Role.admin.name:
#             return True
#         if request.method in permissions.SAFE_METHODS:
#             return True
#         return request.user.role == Role.owner.name and obj.owner == request.user

class HousingPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if not request.user or not request.user.is_authenticated:
            return False
        if request.user.role == Role.admin.name:
            return True
        if request.method == 'POST':
            return request.user.role == Role.owner.name
        return True

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if not request.user or not request.user.is_authenticated:
            return False
        if request.user.role == Role.admin.name:
            return True
        return request.user.role == Role.owner.name and obj.owner == request.user