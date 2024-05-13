import atexit
import logging
from queue import Queue
from logging.handlers import QueueHandler, QueueListener


class ThreadedHandler(QueueHandler):
    def __init__(self, respect_handler_level: bool = True, queue=None, **handlers):
        logging.Handler.__init__(self)
        self.queue = queue if queue is not None else Queue(maxsize=-1)

        self.listener = QueueListener(self.queue, *handlers.values(), respect_handler_level=respect_handler_level)
        self.listener.start()
        atexit.register(self.listener.stop)

    def prepare(self, record: logging.LogRecord) -> logging.LogRecord:
        return record
