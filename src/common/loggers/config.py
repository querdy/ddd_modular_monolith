import logging.config
import sys
from logging.handlers import RotatingFileHandler

from litestar.logging import LoggingConfig
from loguru import logger

from src.common.loggers.filters import ExcludeMetricsFilter
from src.common.loggers.formatters.console import (
    PrettyLitestarConsoleFormatter,
    PrettyFastStreamConsoleFormatter,
    PrettySQLAlchemyConsoleFormatter,
)
from src.common.loggers.formatters.loki import LokiJSONFormatter

litestar_config = LoggingConfig(
    loggers={
        "app": {
            "level": "INFO",
            "handlers": ["file", "console"],
            "propagate": False,
        },
        "uvicorn": {
            "level": "INFO",
            "handlers": ["file", "console"],
            "propagate": False,
        },
    },
    handlers={
        "file": {
            "()": RotatingFileHandler,
            "filename": "/app/logs/app.log",
            "maxBytes": 10 * 1024 * 1024,
            "backupCount": 3,
            "formatter": "json",
        },
        "console": {
            "class": "logging.StreamHandler",
            "stream": sys.stdout,
            "formatter": "console",
            "level": "INFO",
            "filters": ["exclude_metrics"],
        },
    },
    formatters={
        "json": {
            "()": LokiJSONFormatter,
        },
        "console": {
            "()": PrettyLitestarConsoleFormatter,
        },
    },
    filters={
        "exclude_metrics": {
            "()": ExcludeMetricsFilter,
        }
    },
)

log_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "loggers": {
        "faststream": {
            "handlers": ["file", "console"],
            "level": "INFO",
            "propagate": False,
        },
        # "sqlalchemy.engine": {
        #     "handlers": ["sqlalchemy_console"],
        #     "level": "INFO",
        #     "propagate": False,
        # },
    },
    "handlers": {
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "/app/logs/fs.log",
            "maxBytes": 10 * 1024 * 1024,
            "backupCount": 3,
            "formatter": "json",
            "level": "INFO",
        },
        "console": {
            "class": "logging.StreamHandler",
            "stream": sys.stdout,
            "formatter": "console",
            "level": "INFO",
        },
        "sqlalchemy_console": {
            "class": "logging.StreamHandler",
            "stream": sys.stdout,
            "formatter": "sqlalchemy",
            "level": "INFO",
        },
    },
    "formatters": {
        "json": {
            "()": LokiJSONFormatter,
        },
        "console": {
            "()": PrettyFastStreamConsoleFormatter,
        },
        "sqlalchemy": {"()": PrettySQLAlchemyConsoleFormatter},
    },
}

logging.config.dictConfig(log_config)

logger.remove()
logger.add(
    sys.stdout,
    level="TRACE",
    colorize=True,
    format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
)
