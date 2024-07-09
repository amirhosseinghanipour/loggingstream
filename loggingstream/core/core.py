import json
import yaml
import threading
from threading import Thread
from queue import Queue
import time
from typing import List, Optional
import os
from enum import Enum
from ..handlers import Handler
from ..formatters.formatters import Formatter

class LogRecord:
    def __init__(self, name, level, filename, lineno, msg, args, exc_info, func=None, sinfo=None):
        self.name = name
        self.levelname = level
        self.filename = filename
        self.lineno = lineno
        self.msg = msg
        self.args = args
        self.exc_info = exc_info
        self.funcName = func
        self.sinfo = sinfo
        self.created = time.time()
        self.threadName = threading.current_thread().name



class ColoredFormatter(Formatter):
    COLORS = {
        'DEBUG': '\033[94m',    # Blue
        'INFO': '\033[92m',     # Green
        'WARNING': '\033[93m',  # Yellow
        'ERROR': '\033[91m',    # Red
        'CRITICAL': '\033[95m', # Magenta
    }
    RESET = '\033[0m'

    def format(self, record: LogRecord) -> str:
        log_color = self.COLORS.get(record.levelname, self.RESET)
        formatted_message = super().format(record)
        return f"{log_color}{formatted_message}{self.RESET}"

class JSONFormatter(Formatter):
    def format(self, record: LogRecord) -> str:
        log_record = {
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(record.created)),
            'level': record.levelname,
            'message': record.msg,
            'context': {
                'filename': record.filename,
                'lineno': record.lineno,
                'funcName': record.funcName,
                'threadName': record.threadName,
            }
        }
        return json.dumps(log_record)

class YAMLFormatter(Formatter):
    def format(self, record: LogRecord) -> str:
        log_record = {
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(record.created)),
            'level': record.levelname,
            'message': record.msg,
            'context': {
                'filename': record.filename,
                'lineno': record.lineno,
                'funcName': record.funcName,
                'threadName': record.threadName,
            }
        }
        return yaml.dump(log_record)

class StreamHandler(Handler):
    def emit(self, record: LogRecord):
        print(self.formatter.format(record))

class RotatingFileHandler(Handler):
    def __init__(self, filename, maxBytes=1000000, backupCount=3):
        super().__init__()
        self.filename = filename
        self.maxBytes = maxBytes
        self.backupCount = backupCount
        self._open_file()

    def _open_file(self):
        self.file = open(self.filename, 'a')

    def _rotate_file(self):
        self.file.close()
        for i in range(self.backupCount - 1, 0, -1):
            sfn = f"{self.filename}.{i}"
            dfn = f"{self.filename}.{i + 1}"
            if os.path.exists(sfn):
                os.rename(sfn, dfn)
        os.rename(self.filename, f"{self.filename}.1")
        self._open_file()

    def emit(self, record: LogRecord):
        if self.file.tell() + len(self.formatter.format(record)) >= self.maxBytes:
            self._rotate_file()
        self.file.write(self.formatter.format(record) + '\n')
        self.file.flush()

    def close(self):
        self.file.close()

class LogLevel(Enum):
    DEBUG = 'DEBUG'
    INFO = 'INFO'
    WARNING = 'WARNING'
    ERROR = 'ERROR'
    CRITICAL = 'CRITICAL'

class Logger:
    def __init__(self, name: str, level: str = 'DEBUG', handlers: Optional[List[Handler]] = None):
        self.name = name
        self.filename = os.path.basename(__file__)
        self.level = LogLevel[level]
        self.handlers = handlers if handlers else []

    def set_level(self, level: str):
        self.level = LogLevel[level]

    def add_handler(self, handler: Handler):
        self.handlers.append(handler)

    def _log(self, level: LogLevel, msg: str):
        if level.value >= self.level.value:
            record = LogRecord(self.name, level.value, self.filename, 0, msg, None, None)
            for handler in self.handlers:
                handler.handle(record)

    def debug(self, msg: str):
        self._log(LogLevel.DEBUG, msg)

    def info(self, msg: str):
        self._log(LogLevel.INFO, msg)

    def warning(self, msg: str):
        self._log(LogLevel.WARNING, msg)

    def error(self, msg: str):
        self._log(LogLevel.ERROR, msg)

    def critical(self, msg: str):
        self._log(LogLevel.CRITICAL, msg)

class AsyncHandler(Handler):
    def __init__(self, handler: Handler):
        super().__init__()
        self.handler = handler
        self.queue = Queue()
        self.thread = Thread(target=self._process_queue)
        self.thread.daemon = True
        self.thread.start()

    def _process_queue(self):
        while True:
            record = self.queue.get()
            if record is None:
                break
            self.handler.handle(record)

    def emit(self, record: LogRecord):
        self.queue.put(record)

    def close(self):
        self.queue.put(None)
        self.thread.join()
        self.handler.close()
        super().close()

class BatchHandler(Handler):
    def __init__(self, handler: Handler, batch_size=10, flush_interval=5):
        super().__init__()
        self.handler = handler
        self.batch_size = batch_size
        self.flush_interval = flush_interval
        self.buffer = []
        self.last_flush_time = time.time()

    def emit(self, record: LogRecord):
        self.buffer.append(record)
        current_time = time.time()
        if len(self.buffer) >= self.batch_size or (current_time - self.last_flush_time) >= self.flush_interval:
            self.flush()

    def flush(self):
        for record in self.buffer:
            self.handler.handle(record)
        self.buffer = []
        self.last_flush_time = time.time()

    def close(self):
        self.flush()
        self.handler.close()
        super().close()