from logging import Filter, LogRecord

class DevelopmentFilter(Filter):
    def filter(self, record: LogRecord):
        return record.levelname in ("DEBUG", "INFO", "ERROR")