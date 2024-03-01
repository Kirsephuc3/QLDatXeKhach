from rest_framework.permissions import BasePermission
from rest_framework import permissions


class IsAdmin(BasePermission):
    message = "Bạn không có quyền truy cập."

    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        return request.user.is_authenticated and request.user.role == 'admin'


class IsDriver(BasePermission):
    message = "Bạn không có quyền truy cập."

    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        return request.user.role == 'admin' or request.user.role == 'driver'


class IsSeller(BasePermission):
    message = "Bạn không có quyền truy cập này."

    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        return request.user.role == 'admin' or request.user.role == 'ticket seller'


class IsCustomer(BasePermission):
    message = "Bạn không có quyền truy cập này."

    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        return request.user.role == 'admin' or request.user.role == 'user'


class OwnerAuthenticated(permissions.IsAuthenticated):
    def has_objects_permission(self, request, view, obj):
        return self.has_permission(request, view) and request.user == obj.user
