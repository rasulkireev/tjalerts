from .base import *

DJANGO_REQUEST_LOG_LEVEL = os.getenv("DJANGO_REQUEST_LOG_LEVEL", "WARNING")

LOGGING["root"]["handlers"] = ["json"]  # type: ignore

production_structlog_processors = [
    structlog.processors.dict_tracebacks,
]

structlog.configure(
    processors=base_structlog_processors + production_structlog_processors + base_structlog_formatter,  # type: ignore
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)
