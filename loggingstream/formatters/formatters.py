from core.core import LogRecord

class Formatter:
    def format(self, record: LogRecord) -> str:
        return f"{record.created} - {record.name} - {record.levelname} - {record.msg}"