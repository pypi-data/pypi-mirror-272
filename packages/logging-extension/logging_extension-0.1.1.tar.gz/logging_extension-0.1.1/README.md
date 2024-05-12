### JSONFormatter
Format logs as JSON lines
### ThreadedHandler
Container of handlers for logging in a separate thread

### Configuration example
#### in code


```python
import logging
from logging_extension import ThreadedHandler, JSONFormatter

logging.basicConfig(level=logging.DEBUG)
logging.getLogger().handlers.clear()

handler = logging.StreamHandler()
formatter = JSONFormatter(fmt_keys=dict(
    logger='name',
    level='levelno'
))

handler.setFormatter(formatter)
threaded_handler = ThreadedHandler(stream_handler=handler)

logging.getLogger().addHandler(threaded_handler)
logging.getLogger().debug('debug_msg', extra={'extra': 'value'})
```

    {"logger": "root", "level": 10, "created": "2024-05-11T16:48:30.478645+00:00", "message": "debug_msg", "extra": "value"}


#### via config


```python
import logging.config

# Usually defined in .json or .yml file
config = {
    "version": 1,
    "disable_existing_handlers": False,
    "formatters": {
        "json_formatter": {
            "()": "logging_extension.JSONFormatter",
            "fmt_keys": {
                "name": "name",
                "level": "levelno",
                "line": "lineno"
            }
        }
    },
    "handlers": {
        "stream_handler": {
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
            "formatter": "json_formatter"
        },
        "threaded_handler": {
            "()": "logging_extension.ThreadedHandler",
            "stream_handler": "cfg://handlers.stream_handler"
        }
    },
    "loggers": {
        "root": {
            "level": "DEBUG",
            "handlers": [
                "threaded_handler"
            ]
        }
    }
}

logging.config.dictConfig(config)
logging.getLogger().debug('debug_msg', extra={'extra': 'value'})
```

    {"name": "root", "level": 10, "line": 39, "created": "2024-05-11T16:48:30.485113+00:00", "message": "debug_msg", "extra": "value"}

