import logging


class ExcludeMetricsFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        return "/metrics" not in str(record.getMessage())
