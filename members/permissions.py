from rest_framework.permissions import BasePermission, DjangoModelPermissions


class MemberPermissions(BasePermission):
    def has_object_permission(self, request, view, obj):
        permissions = DjangoModelPermissions()
        # TODO: add some extra logic here to make users able to partly edit his/her own details.
        return permissions.has_permission(request, view)
