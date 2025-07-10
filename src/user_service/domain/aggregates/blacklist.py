from dataclasses import dataclass
from datetime import datetime, UTC
from typing import Self
from uuid import UUID, uuid4


@dataclass
class BlacklistedToken:
    id: UUID
    token: str
    expires_at: datetime
    created_at: datetime
    reason: str | None

    @classmethod
    def create(cls, token: str, expires_at: datetime, reason: str | None = None) -> Self:
        if isinstance(expires_at, int):
            expires_at = datetime.fromtimestamp(expires_at)
        return cls(
            id=uuid4(),
            token=token,
            expires_at=expires_at,
            created_at=datetime.now(UTC).replace(tzinfo=None),
            reason=reason,
        )
