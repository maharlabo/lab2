from datetime import datetime
from pydantic import BaseModel
from typing import Literal

class LoggingEntry(BaseModel):
    timestamp: datetime
    level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    source: str
    message: str