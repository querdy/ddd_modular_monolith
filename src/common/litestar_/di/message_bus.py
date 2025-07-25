from dishka import Provider, Scope, provide

from src.common.message_bus.broker import broker
from src.common.message_bus.interfaces import IMessageBus
from src.common.message_bus.message_bus import FastStreamMessageBus


class MessagingProvider(Provider):
    @provide(scope=Scope.APP)
    def message_bus(self) -> IMessageBus:
        return FastStreamMessageBus(broker)
