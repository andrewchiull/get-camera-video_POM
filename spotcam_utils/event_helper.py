import os
from datetime import datetime
import logging
from typing import Optional, Any
from enum import Enum

from pydantic import BaseModel

class Status(Enum):
    DEFAULT = 0

    REQUESTED = 10
    REQUESTED_EMPTY_ONCE = 11
    REQUESTED_EMPTY_TWICE = 12

    GENERATED = 20
    GENERATED_FAILED = 21

    DOWNLOADED = 30
    DOWNLOADED_FAILED = 31

    RENAMED = 40
    RENAMED_FAILED = 41

    UPLOADED = 50
    UPLOADED_FAILED = 51

    ERASED = 60
    ERASED_FAILED = 61

class EventHelper(BaseModel):
    time: Optional[datetime]
    status = Status.DEFAULT

    def __repr__(self):
        return f'{self.time} | {self.status}'