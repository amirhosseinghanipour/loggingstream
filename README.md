# LoggingStream

`LoggingStream` is a flexible and powerful logging library for Python, designed to provide a variety of logging handlers, formatters, and levels. It supports features like rotating file handlers, colored console output, JSON and YAML formatting, asynchronous logging, and batch logging.

## Features

- **Multiple Logging Levels**: DEBUG, INFO, WARNING, ERROR, CRITICAL
- **Handlers**: StreamHandler, RotatingFileHandler, AsyncHandler, BatchHandler
- **Formatters**: Plain text, Colored, JSON, YAML
- **Thread Safety**: Ensures safe logging in multi-threaded applications
- **Configuration**: Easy configuration from environment variables

## Installation

* The library is still under development and not yet ready for production use.
~~You can install `LoggingStream` via pip:~~

```sh
~~pip install loggingstream~~
```

## Usage

### Basic Usage

```python
from loggingstream.core import Logger, LogLevel
from loggingstream.handlers import StreamHandler
from loggingstream.formatters import Formatter

# Create a logger
logger = Logger(name="my_logger", filename="app.log", level=LogLevel.DEBUG)

# Create a console handler with colored output
console_handler = StreamHandler()
console_handler.setFormatter(Formatter())

# Add the handler to the logger
logger.addHandler(console_handler)

# Log messages
logger.debug("This is a debug message")
logger.info("This is an info message")
logger.warning("This is a warning message")
logger.error("This is an error message")
logger.critical("This is a critical message")
```

### Rotating File Handler

```python
from loggingstream.handlers import RotatingFileHandler
from loggingstream.formatters import JSONFormatter

# Create a rotating file handler
file_handler = RotatingFileHandler(filename="app.log", maxBytes=1000000, backupCount=3)
file_handler.setFormatter(JSONFormatter())

# Add the handler to the logger
logger.addHandler(file_handler)
```

### Asynchronous Logging

```python
from loggingstream.handlers.handlers import AsyncHandler

# Create an async handler
async_handler = AsyncHandler(console_handler)

# Add the async handler to the logger
logger.addHandler(async_handler)
```

### Batch Logging

```python
from loggingstream.handlers.handlers import BatchHandler

# Create a batch handler
batch_handler = BatchHandler(file_handler, batch_size=10, flush_interval=5)

# Add the batch handler to the logger
logger.addHandler(batch_handler)
```

### Configuration from Environment Variables

```python
import os
from loggingstream.core.core import Logger

# Set environment variables
os.environ['LOGGER_NAME'] = 'env_logger'
os.environ['LOGGER_FILENAME'] = 'env_app.log'
os.environ['LOGGER_LEVEL'] = 'DEBUG'

# Create a logger from environment variables
logger = Logger.from_env()
```

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- Inspired by Python's built-in logging module.