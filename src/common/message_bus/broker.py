from faststream.rabbit import RabbitBroker
from loguru import logger

broker = RabbitBroker("amqp://user:password@rabbitmq:5672", logger=logger)
