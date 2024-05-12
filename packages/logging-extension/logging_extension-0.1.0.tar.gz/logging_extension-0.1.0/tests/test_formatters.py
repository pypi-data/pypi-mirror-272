import io
import json
import logging
from unittest import TestCase
from src.logging_extension.formatters import JSONFormatter


logging.basicConfig(level=logging.DEBUG)


class TestJSONFormatter(TestCase):
    def setUp(self):
        logging.getLogger().handlers.clear()
        self.logger = logging.getLogger()

        self.stream = io.StringIO()
        self.handler = logging.StreamHandler(stream=self.stream)
        self.logger.addHandler(self.handler)

    def test_always_fields(self):
        self.handler.setFormatter(JSONFormatter())
        self.logger.debug('debug_message', exc_info=True, stack_info=True)

        self.stream.seek(0)
        log_dict = json.load(self.stream)
        self.assertSetEqual({'created', 'message', 'exc_info', 'stack_info'}, set(log_dict))

    def test_fmt_keys(self):
        fmt_keys = dict(
            message='message',
            module='module',
            func='funcName',
            line='lineno',
        )
        self.handler.setFormatter(JSONFormatter(fmt_keys=fmt_keys))
        self.logger.debug('debug_message')

        self.stream.seek(0)
        log_dict = json.load(self.stream)
        self.assertSetEqual({'created', 'message', 'module', 'func', 'line'}, set(log_dict))

    def test_extra(self):
        extra = {'custom_key': 'value'}
        self.handler.setFormatter(JSONFormatter())
        self.logger.debug('debug_message', extra=extra)

        self.stream.seek(0)
        log_dict = json.load(self.stream)
        self.assertSetEqual({'created', 'message', 'custom_key'}, set(log_dict))
        self.assertEqual(log_dict['custom_key'], extra['custom_key'])
