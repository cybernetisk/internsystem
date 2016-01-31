from rest_framework.permissions import BasePermission, SAFE_METHODS


class VaretellingPermissions(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return not obj.is_locked


class VaretellingVarePermissions(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return not obj.varetelling.is_locked
