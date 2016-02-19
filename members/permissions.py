from rest_framework.permissions import BasePermission, DjangoModelPermissions

from members.models import Member


def has_permission(request, instance, type):
    return request.user.has_perm('%s.%s.%s' % (Member._meta.app_label, type, Member._meta.model_name))


class MemberPermissions(BasePermission):
    def has_object_permission(self, request, view, obj):
        permissions = DjangoModelPermissions()
        # TODO: add some extra logic here to make users able to partly edit his/her own details.
        return permissions.has_permission(request, view)
