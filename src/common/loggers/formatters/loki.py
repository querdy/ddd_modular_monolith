import json
import logging
from datetime import datetime, UTC

from src.common.loggers.formatters.colors import COLOR_MAP, RESET


class LokiJSONFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        timestamp = datetime.fromtimestamp(record.created, UTC).isoformat()
        level_color = COLOR_MAP.get(record.levelname, "")
        level_colored = f"{level_color}{record.levelname:<8}{RESET}"
        formatted = f"{level_colored} | {record.name}:{record.funcName}:{record.lineno} - {record.getMessage()}"

        log = {
            "timestamp": timestamp,
            "level": record.levelname,
            "logger": record.name,
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
            "message": record.getMessage(),
            "formatted": formatted,
        }
        return json.dumps(log)
