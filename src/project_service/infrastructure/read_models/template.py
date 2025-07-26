from pydantic import BaseModel, ConfigDict


class StageTemplateRead(BaseModel):
    name: str
    description: str

    model_config = ConfigDict(from_attributes=True)


class SubprojectTemplateRead(BaseModel):
    stages: list[StageTemplateRead]

    model_config = ConfigDict(from_attributes=True)
