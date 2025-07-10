from uuid import UUID

from dishka import FromDishka
from dishka.integrations.litestar import inject
from litestar import Controller, post

from src.project_service.application.protocols import IProjectServiceUoW
from src.project_service.application.use_cases.write.stage import CreateStageUseCase
from src.project_service.domain.entities.stage import Stage


class StagesController(Controller):
    path = "/stages"
    tags = ["Этапы"]

    @post(path="", summary="Добавление этапа к подпроекту")
    @inject
    async def create(self, uow: FromDishka[IProjectServiceUoW]) -> Stage:
        use_case = CreateStageUseCase(uow)
        a = "c2690e12-ff22-4a92-b7fb-48310088742e"
        result = await use_case.execute(UUID(a), "kekw", "???")
        return result