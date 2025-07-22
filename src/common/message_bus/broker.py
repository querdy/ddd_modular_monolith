import logging

from faststream.rabbit import RabbitBroker

broker = RabbitBroker(
    "amqp://user:password@rabbitmq:5672",
    logger=logging.getLogger("faststream"),
)
