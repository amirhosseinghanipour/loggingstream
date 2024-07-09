from loggingstream.core.core import Logger
from loggingstream.core.handlers import StreamHandler, RotatingFileHandler, AsyncHandler, BatchHandler
from loggingstream.core.formatters import ColoredFormatter, JSONFormatter

def main():
    logger = Logger("test")
    logger.set_level('DEBUG')

    console_handler = StreamHandler()
    console_handler.set_formatter(ColoredFormatter())

    file_handler = RotatingFileHandler("loggings.log", maxBytes=1000000, backupCount=3)
    file_handler.set_formatter(JSONFormatter())

    async_console_handler = AsyncHandler(console_handler)
    batch_file_handler = BatchHandler(file_handler)

    logger.add_handler(async_console_handler)
    logger.add_handler(batch_file_handler)

    logger.info("This is an info message")
    logger.error("This is an error message")

    for handler in logger.handlers:
        handler.close()

if __name__ == "__main__":
    main()