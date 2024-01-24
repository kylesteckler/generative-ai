# Helper classes for Cloud Run logging.
# https://cloud.google.com/run/docs/logging

from pydantic import BaseModel
from enum import Enum
from typing import Dict, Any, Optional
import sys

class SeverityEnum(str, Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

class StatusMessage(BaseModel):
    severity: SeverityEnum
    message: str
    data: Dict[str, Any] | None = None

    def log(self):
        print(self.model_dump_json(exclude_none=True))
        sys.stdout.flush() # Need to flush stdout otherwise large delays


class Logger:
    def info(self, msg: str, **kwargs):
        if not kwargs:
            kwargs = None
        log_msg = StatusMessage(
            severity=SeverityEnum.INFO,
            message=msg,
            data=kwargs
        )
        log_msg.log()

    def warning(self, msg: str, **kwargs):
        if not kwargs:
            kwargs = None
        log_msg = StatusMessage(
            severity=SeverityEnum.WARNING,
            message=msg,
            data=kwargs
        )
        log_msg.log()

    def error(self, msg: str, **kwargs):
        if not kwargs:
            kwargs = None
        log_msg = StatusMessage(
            severity=SeverityEnum.ERROR,
            message=msg,
            data=kwargs
        )
        log_msg.log()

    def critical(self, msg: str, **kwargs):
        if not kwargs:
            kwargs = None
        log_msg = StatusMessage(
            severity=SeverityEnum.CRITICAL,
            message=msg,
            data=kwargs
        )
        log_msg.log()

logger = Logger()
