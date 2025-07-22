import logging
from datetime import UTC, datetime

from src.loggers.formatters.colors import COLOR_MAP, RESET


class PrettyLitestarConsoleFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        dt = datetime.fromtimestamp(record.created, tz=UTC)
        timestamp = dt.strftime("%Y-%m-%d %H:%M:%S") + f".{int(dt.microsecond / 1000):03d}"
        level_color = COLOR_MAP.get(record.levelname, "")
        level_colored = f"{level_color}{record.levelname}{RESET}"
        return f"{timestamp} [{level_colored}] {record.name}:{record.funcName}:{record.lineno} - {record.getMessage()}"


class PrettyFastStreamConsoleFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        dt = datetime.fromtimestamp(record.created, tz=UTC)
        timestamp = dt.strftime("%Y-%m-%d %H:%M:%S") + f".{int(dt.microsecond / 1000):03d}"
        level_color = COLOR_MAP.get(record.levelname, "")
        level_colored = f"{level_color}{record.levelname}{RESET}"
        return f"{timestamp} [{level_colored}] {record.name}:{record.funcName}:{record.lineno} - | {record.queue} | - {record.getMessage()}"
