from core.utils import SharedAPIRootRouter

from intern.rest import (
    InternViewSet,
    InternGroupViewSet,
    AccessLevelViewSet,
    RoleViewSet,
    InternRoleViewSet,
)

# SharedAPIRootRouter is automatically imported in global urls config
router = SharedAPIRootRouter()
router.register(r"intern/interns", InternViewSet, basename="interns")
router.register(r"intern/groups", InternGroupViewSet, basename="interngroups")
router.register(r"intern/accesslevels", AccessLevelViewSet, basename="accesslevels")
router.register(r"intern/roles", RoleViewSet, basename="roles")
router.register(r"intern/internroles", InternRoleViewSet, basename="internroles")
