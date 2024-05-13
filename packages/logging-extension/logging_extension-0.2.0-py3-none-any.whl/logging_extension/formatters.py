import json
import logging
from datetime import datetime, timezone


LOG_RECORD_BUILTIN_ATTRS = {
    'args',
    'asctime',
    'created',
    'exc_info',
    'filename',
    'funcName',
    'levelname',
    'levelno',
    'lineno',
    'message',
    'module',
    'msg',
    'name',
    'pathname',
    'process',
    'processName',
    'relativeCreated',
    'stack_info',
    'thread',
    'threadName',
    'taskName',
    'exc_text',
    'msecs',
}


class JSONFormatter(logging.Formatter):
    def __init__(self, *, fmt_keys: dict[str, str] | None = None):
        super().__init__()
        self._fmt_keys = fmt_keys if fmt_keys is not None else {}

    def format(self, record: logging.LogRecord) -> str:
        message = self._prepare_message(record)
        self._add_extra(message, record)
        return json.dumps(message, default=str)

    def _prepare_message(self, record: logging.LogRecord) -> dict:
        always_fields = dict(
            created=datetime.fromtimestamp(record.created, tz=timezone.utc).isoformat(),
            message=record.getMessage(),
        )
        if record.exc_info is not None:
            always_fields['exc_info'] = self.formatException(record.exc_info)

        if record.stack_info is not None:
            always_fields['stack_info'] = self.formatStack(record.stack_info)

        message = {key: msg_val
                   if (msg_val := always_fields.pop(val, None)) is not None
                   else getattr(record, val)
                   for key, val in self._fmt_keys.items()
                   }
        message.update(always_fields)
        return message

    def _add_extra(self, message: dict, record: logging.LogRecord) -> None:
        for key, val in record.__dict__.items():
            if key not in LOG_RECORD_BUILTIN_ATTRS:
                message[key] = val
