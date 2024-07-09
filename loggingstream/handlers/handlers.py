from core.core import LogRecord
from formatters.formatters import Formatter

class Handler:
    def __init__(self):
        self.formatter = Formatter()

    def set_formatter(self, formatter: Formatter):
        self.formatter = formatter

    def handle(self, record: LogRecord):
        self.emit(record)

    def emit(self, record: LogRecord):
        raise NotImplementedError("emit must be implemented by Handler subclasses")

    def close(self):
        pass