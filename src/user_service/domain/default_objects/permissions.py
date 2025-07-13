from src.user_service.domain.aggregates.permission import Permission

default_permissions = [
    Permission.create(code="role_read", description="Право на чтение ролей"),
    Permission.create(code="role_write", description="Право на изменение ролей"),
    Permission.create(code="user_read", description="Право на чтение пользователя"),
    Permission.create(code="user_write", description="Право на изменение пользователя"),
]
