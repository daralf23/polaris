from __future__ import annotations

import logging
import sys

import structlog

from polaris.models.plugin_log import PluginLog


class LoggerService:
    def __init__(self):

        logging.basicConfig(
            format="%(message)s",
            stream=sys.stdout,
            level=logging.INFO,
        )

        structlog.configure(
            processors=[
                structlog.processors.TimeStamper(fmt="iso"),
                structlog.processors.add_log_level,
                structlog.processors.JSONRenderer(),
            ],
            wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
        )

        self._logger = structlog.get_logger()

    def debug(self, event: str, **fields):
        self._logger.debug(event, **fields)

    def info(self, event: str, **fields):
        self._logger.info(event, **fields)

    def warning(self, event: str, **fields):
        self._logger.warning(event, **fields)

    def error(self, event: str, **fields):
        self._logger.error(event, **fields)

    def exception(self, event: str, **fields):
        self._logger.exception(event, **fields)

    def telemetry(self, log: PluginLog):
        self._logger.info(
            "plugin_execution",
            **log.to_json(),
        )
