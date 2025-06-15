from functools import singledispatch

from src.user_service.domain.aggregates.role import Role
from src.user_service.domain.enities.permission import Permission
from src.user_service.domain.value_objects.permission_code import PermissionCode
from src.user_service.domain.value_objects.permission_description import PermissionDescription
from src.user_service.domain.value_objects.role_name import RoleName
from src.user_service.infrastructure.db.postgres.models import RoleModel, PermissionModel


@singledispatch
def role_to_domain(obj):
    raise NotImplementedError(f"No mapper for type: {type(obj)}")

@role_to_domain.register
def _(obj: RoleModel) -> Role:
    permissions = [permission_to_domain(p) for p in obj.permissions]
    return Role(
        id=obj.id,
        name=RoleName(obj.name),
        permissions=permissions
    )

@singledispatch
def permission_to_domain(obj):
    raise NotImplementedError(f"No mapper for type: {type(obj)}")

@permission_to_domain.register
def _(obj: PermissionModel) -> Permission:
    return Permission(
        id=obj.id,
        code=PermissionCode(obj.name),
        description=PermissionDescription(obj.description)
    )