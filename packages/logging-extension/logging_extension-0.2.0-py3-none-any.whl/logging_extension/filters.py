import logging


class BelowLevelFilter(logging.Filter):
    def __init__(self, level: str | int, name: str = ''):
        super().__init__(name=name)
        self.level = level if isinstance(level, int) else logging.getLevelName(level)

    def filter(self, record: logging.LogRecord) -> bool:
        return record.levelno < self.level
