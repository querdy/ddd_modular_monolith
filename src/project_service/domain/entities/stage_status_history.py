from dataclasses import dataclass
from datetime import datetime, UTC
from typing import Self
from uuid import UUID, uuid4

from src.project_service.domain.value_objects.enums import StageStatus


@dataclass
class StageStatusHistory:
    id: UUID
    stage_id: UUID
    to_status: StageStatus
    changed_by: UUID
    changed_at: datetime

    @classmethod
    def create(
        cls,
        stage_id: UUID,
        changed_by: UUID,
        to_status: StageStatus,
        changed_at: datetime | None = None,
    ) -> Self:
        return cls(
            id=uuid4(),
            stage_id=stage_id,
            to_status=to_status,
            changed_by=changed_by,
            changed_at=datetime.now(UTC).replace(tzinfo=None) if changed_at is None else changed_at,
        )
