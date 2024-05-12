import io
import time
import logging.config
from unittest import TestCase
from src.logging_extension.handlers import ThreadedHandler


logging.basicConfig(level=logging.DEBUG)


class TestThreadedHandler(TestCase):
    def setUp(self):
        logging.getLogger().handlers.clear()

    def _assert_write(self, stream: io.IOBase, message: str, expire_sec=1):
        start = time.perf_counter()
        while not stream.tell() and time.perf_counter() - start <= expire_sec:
            time.sleep(0.01)

        stream.seek(0)
        self.assertEqual(stream.readline().rstrip(), message)

    def test_code_configure(self):
        stream = io.StringIO()
        handler = ThreadedHandler(handler_0=logging.StreamHandler(stream=stream))
        logging.getLogger().addHandler(handler)
        logging.getLogger().debug('debug_msg')

        self._assert_write(stream, 'debug_msg')

    def test_config_configure(self):
        stream = io.StringIO()
        config = {
            "version": 1,
            "disable_existing_handlers": False,
            "handlers": {
                "default": {
                    "class": "logging.StreamHandler",
                    "stream": stream
                },
                "threaded_handler": {
                    "()": ThreadedHandler,
                    "handler_0": "cfg://handlers.default"
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
        logging.getLogger().debug('config_msg')

        self._assert_write(stream, 'config_msg')
