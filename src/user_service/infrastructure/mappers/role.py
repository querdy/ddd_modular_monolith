from functools import singledispatch

from src.user_service.domain.aggregates.role import Role
from src.user_service.domain.enities.permission import Permission
from src.user_service.domain.value_objects.permission_code import PermissionCode
from src.user_service.domain.value_objects.permission_description import (
    PermissionDescription,
)
from src.user_service.domain.value_objects.role_name import RoleName
from src.user_service.infrastructure.db.postgres.models import (
    RoleModel,
    PermissionModel,
)


@singledispatch
def role_to_domain(obj):
    raise NotImplementedError(f"No mapper for type: {type(obj)}")


@role_to_domain.register
def _(obj: RoleModel) -> Role:
    permissions = [permission_to_domain(p) for p in obj.permissions]
    return Role(id=obj.id, name=RoleName(obj.name), permissions=permissions)


@singledispatch
def role_to_orm(obj: Role) -> RoleModel:
    raise NotImplementedError(f"No orm mapper for {type(obj)}")


@role_to_orm.register
def _(obj: Role) -> RoleModel:
    return RoleModel(
        id=obj.id,
        name=obj.name,
        permissions=[permission_to_orm(permission) for permission in obj.permissions],
    )


@singledispatch
def permission_to_domain(obj):
    raise NotImplementedError(f"No mapper for type: {type(obj)}")


@permission_to_domain.register
def _(obj: PermissionModel) -> Permission:
    return Permission(
        id=obj.id,
        code=PermissionCode(obj.code),
        description=PermissionDescription(obj.description),
    )


@singledispatch
def permission_to_orm(obj: Permission) -> PermissionModel:
    return PermissionModel(
        id=obj.id,
        code=obj.code,
        description=obj.description,
    )
