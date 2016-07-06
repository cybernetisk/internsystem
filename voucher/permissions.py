import datetime
from rest_framework.permissions import BasePermission, DjangoModelPermissions

from voucher.models import VoucherRegisterLog


def register_log_has_perm(request, obj, perm_action=None):
    """Check for permission to modify work log. perm_action can be change or delete"""
    if obj.is_locked():
        return False

    if perm_action is not None:
        if request.user.has_perm('%s.%s_%s' % (VoucherRegisterLog._meta.app_label, perm_action, VoucherRegisterLog._meta.model_name)):
            return True

    if obj.issuing_user != request.user:
        return False

    return True


class RegisterLogPermissions(BasePermission):
    def has_object_permission(self, request, view, obj):
        if view.action not in ['update', 'partial_update', 'destroy']:
            return True

        modelperm = DjangoModelPermissions()
        if modelperm.has_permission(request, view):
            return True

        return register_log_has_perm(request, obj)
