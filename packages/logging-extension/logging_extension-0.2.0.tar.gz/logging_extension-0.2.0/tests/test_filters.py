import logging.config
from unittest import TestCase
from src.logging_extension.filters import BelowLevelFilter


class TestBelowLevelFilter(TestCase):
    def test_filter(self):
        level_filter = BelowLevelFilter(level=logging.ERROR)
        logging.getLogger().addFilter(level_filter)

        with self.assertLogs():
            logging.getLogger().warning('warning_msg')
        with self.assertNoLogs():
            logging.getLogger().error('error_msg')
