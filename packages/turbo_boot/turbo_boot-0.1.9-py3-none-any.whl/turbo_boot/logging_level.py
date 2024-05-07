from enum import Enum


class LoggingLevel(Enum):
    NOSET = 0
    DEBUG = 10
    INFO = 20
    WARN = 30
    ERROR = 40
    CRITICAL = 50
