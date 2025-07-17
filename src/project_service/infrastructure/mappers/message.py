from functools import singledispatch

from src.project_service.domain.entities.message import Message
from src.project_service.domain.value_objects.message_text import MessageText
from src.project_service.infrastructure.db.postgres.models import MessageModel


@singledispatch
def message_to_orm(obj) -> MessageModel:
    raise NotImplementedError(f"No orm mapper for {type(obj)}")


@message_to_orm.register
def _(obj: Message) -> MessageModel:
    return MessageModel(id=obj.id, created_at=obj.created_at, author_id=obj.author_id, text=obj.text)


@singledispatch
def message_to_domain(obj) -> Message:
    raise NotImplementedError(f"No domain mapper for {type(obj)}")


@message_to_domain.register
def _(obj: MessageModel) -> Message:
    return Message(id=obj.id, created_at=obj.created_at, author_id=obj.author_id, text=MessageText(obj.text))
