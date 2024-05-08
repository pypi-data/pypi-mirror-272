import uuid
from contextvars import ContextVar

# See also: https://github.com/snok/asgi-correlation-id
TRACE_ID_VAR: ContextVar[str | None] = ContextVar("trace_id", default=None)


def new_trace_id(subprefix: str, prefix: str = "cc", total_len: int = 16) -> str:
    uuid_len = total_len - len(prefix) - len(subprefix)
    return prefix + subprefix + uuid.uuid4().hex[:uuid_len]
