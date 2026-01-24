"""Logging Module.

Structured logging configuration for Nexus.
"""

import structlog

from nexus.config.settings import settings


def configure_logging() -> None:
    """Configure Structured Logging.

    Sets up structlog with appropriate processors.

    Args:
        None

    Returns:
        None

    Raises:
        None
    """

    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.dev.ConsoleRenderer() if settings.debug else structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(getattr(structlog.stdlib, settings.log_level)),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )


configure_logging()
logger: structlog.stdlib.BoundLogger = structlog.get_logger()


__all__: list[str] = ["configure_logging", "logger"]
