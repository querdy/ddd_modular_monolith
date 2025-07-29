from dataclasses import asdict

from dishka import FromDishka
from dishka.integrations.faststream import inject
from loguru import logger

from src.common.message_bus.broker import broker
from src.project_service.application.events.stage import StageStatusChangedEvent
from src.project_service.application.protocols import IProjectServiceUoW
from src.project_service.domain.entities.stage_status_history import StageStatusHistory


@broker.subscriber("stagestatuschangedevent")
@inject
async def on_stage_status_changed(event: StageStatusChangedEvent, uow: FromDishka[IProjectServiceUoW]):
    async with uow:
        await uow.stage_status_history.add(StageStatusHistory.create(**event.model_dump()))
