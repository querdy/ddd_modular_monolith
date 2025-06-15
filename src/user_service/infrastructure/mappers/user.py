from functools import singledispatch

from src.user_service.domain.aggregates.user import User
from src.user_service.domain.enities.user_role_assignment import UserRoleAssignment
from src.user_service.domain.value_objects.email import Email
from src.user_service.domain.value_objects.hashed_password import HashedPassword
from src.user_service.domain.value_objects.username import Username
from src.user_service.infrastructure.db.postgres.models import UserModel, UserRoleAssignmentModel


@singledispatch
def user_to_domain(obj):
    raise NotImplementedError(f"No domain mapper for {type(obj)}")

@user_to_domain.register
def _(obj: UserModel) -> User:
    return User(
        id=obj.id,
        username=Username(obj.username),
        email=Email(obj.email),
        hashed_password=HashedPassword(obj.hashed_password),
        role_assignments=user_role_assignment_to_domain(obj.role_assignments),
    )

@singledispatch
def user_role_assignment_to_domain(obj):
    raise NotImplementedError(f"No domain mapper for {type(obj)}")

@user_role_assignment_to_domain.register
def _(obj: UserRoleAssignmentModel) -> UserRoleAssignment:
        return UserRoleAssignment(
            id=obj.id,
            role_id=obj.role.id,
            assigned_at=obj.assigned_at,
            expires_at=obj.expires_at
        )
