from rest_framework.permissions import BasePermission,DjangoModelPermissions

class CardPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        if request.user is obj.user:
            return True

        return DjangoModelPermissions().has_object_permission(request,view,obj)

    def has_permission(self, request, view):
        return DjangoModelPermissions().has_permission(request, view)