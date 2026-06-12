from rest_framework.permissions import BasePermission

class RolePermission(BasePermission):
    role = None

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == self.role
        )


class IsAdmin(RolePermission):
    role = "admin"


class IsGuide(RolePermission):
    role = "guide"


class IsCustomer(RolePermission):
    role = "customer"