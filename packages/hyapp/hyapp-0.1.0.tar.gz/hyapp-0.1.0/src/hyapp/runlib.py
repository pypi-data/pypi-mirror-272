import asyncio
import enum
import logging
import socket
from typing import Any, ClassVar

from .trace import TRACE_ID_VAR

HOSTNAME = socket.gethostname()


class NotAvailable(enum.Enum):
    NOT_AVAILABLE = "NOT_AVAILABLE"


NOT_AVAILABLE = NotAvailable.NOT_AVAILABLE


class Annotator(logging.Filter):
    """A convenience abstract class for most annotators"""

    default_attribute_name: ClassVar[str | None] = None
    attribute_name: str
    force_overwrite: bool = False

    def __init__(self, *args: Any, attribute_name: str | None = None, **kwargs: Any) -> None:
        if not attribute_name:
            if not self.default_attribute_name:
                raise TypeError("attribute_name should either be on class or always specified")
            attribute_name = self.default_attribute_name
        self.attribute_name = attribute_name
        super().__init__(*args, **kwargs)

    def get_value(self, record: logging.LogRecord) -> Any:
        raise NotImplementedError

    def filter(self, record: logging.LogRecord) -> bool:
        """“annotate”, actually"""
        if hasattr(record, self.attribute_name) and not self.force_overwrite:
            return True
        value = self.get_value(record)
        setattr(record, self.attribute_name, value)
        return True


class HostnameAnnotator(Annotator):
    default_attribute_name: ClassVar[str] = "hostname"

    def get_value(self, record: logging.LogRecord) -> str:
        return HOSTNAME


class AsyncioTaskAnnotator(Annotator):
    default_attribute_name: ClassVar[str] = "aio_task"

    def get_value(self, record: logging.LogRecord) -> str | None:
        try:
            task = asyncio.current_task()
            if task:
                return task.get_name()
        except RuntimeError:
            pass

        return None


class TraceVarAnnotator(Annotator):
    default_attribute_name: ClassVar[str] = "trace_id"

    def get_value(self, record: logging.LogRecord) -> str | None:
        return TRACE_ID_VAR.get()
