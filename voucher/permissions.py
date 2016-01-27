import datetime
from rest_framework.permissions import BasePermission, DjangoModelPermissions

from voucher.models import WorkLog


def work_log_has_perm(request, obj, perm_action=None):
    """Check for permission to modify work log. perm_action can be change or delete"""
    if perm_action is not None:
        if request.user.has_perm('%s.%s_%s' % (WorkLog._meta.app_label, perm_action, WorkLog._meta.model_name)):
            return True

    if obj.issuing_user != request.user:
        return False

    if obj.is_locked():
        return False

    return True


class WorkLogPermissions(BasePermission):
    def has_object_permission(self, request, view, obj):
        if view.action not in ['update', 'partial_update', 'destroy']:
            return True

        modelperm = DjangoModelPermissions()
        if modelperm.has_permission(request, view):
            return True

        return work_log_has_perm(request, obj)
