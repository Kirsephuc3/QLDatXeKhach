from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    message = "Bạn không có quyền truy cập."

    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        return request.user.is_authenticated and request.user.role == 'admin'


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
