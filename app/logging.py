from __future__ import annotations
import logging
import structlog
from structlog.contextvars import merge_contextvars, bind_contextvars, clear_contextvars
logger = structlog.get_logger()
def configure_logging() -> None:
    logging.basicConfig(format='%(message)s', level=logging.INFO)
    structlog.configure(
        processors=[
            merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt='iso'),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.JSONRenderer(),
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
def bind_request_context(**kwargs):
    bind_contextvars(**kwargs)
def clear_request_context():
    clear_contextvars()
