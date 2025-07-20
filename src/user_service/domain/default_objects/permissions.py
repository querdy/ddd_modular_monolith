from src.user_service.domain.enities.permission import Permission

default_permissions = [
    Permission.create(code="roles:read", description="Право на чтение ролей"),
    Permission.create(code="roles:write", description="Право на изменение ролей"),
    Permission.create(code="users:read", description="Право на чтение пользователя"),
    Permission.create(code="users:write", description="Право на изменение пользователя"),
    Permission.create(code="projects:read", description="Право на чтение проектов"),
    Permission.create(code="projects:write", description="Право на изменение проектов"),
    Permission.create(code="subprojects:read", description="Право на чтение подпроектов"),
    Permission.create(code="subprojects:write", description="Право на изменение подпроектов"),
    Permission.create(code="stages:read", description="Право на чтение этапов"),
    Permission.create(code="stages:write", description="Право на изменение этапов"),
    Permission.create(code="stages:change_status_to_completed", description="Право на завершение этапа"),
    Permission.create(code="stages:change_status_to_confirmed", description="Право на выполнение этапа"),
]
