from dataclasses import dataclass
from datetime import datetime, UTC
from typing import Self
from uuid import UUID, uuid4


@dataclass(slots=True)
class UserRoleAssignment:
    id: UUID
    role_id: UUID
    assigned_at: datetime
    expires_at: datetime | None

    @classmethod
    def create(cls, role_id: UUID, expires_at: datetime | None = None) -> Self:
        now = datetime.now(UTC).replace(tzinfo=None)
        return cls(id=uuid4(), role_id=role_id, assigned_at=now, expires_at=expires_at)

    def is_expire(self, at: datetime | None = None) -> bool:
        now = at or datetime.now(UTC).replace(tzinfo=None)
        return self.expires_at is None or (self.assigned_at <= now <= self.expires_at)
