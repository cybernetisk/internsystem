import datetime
from rest_framework.permissions import BasePermission, DjangoModelPermissions

from voucher.models import WorkLog


class WorkLogPermissions(BasePermission):
    def has_object_permission(self, request, view, obj):
        if view.action not in ['update', 'partial_update', 'destroy']:
            return True

        modelperm = DjangoModelPermissions()
        if modelperm.has_permission(request, view):
            return True

        if obj.issuing_user != request.user:
            return False

        now = datetime.datetime.now(datetime.timezone.utc)
        if (now - obj.date_issued).days > WorkLog.LOCKED_FOR_EDITING_AFTER_DAYS:
            return False

        return True
