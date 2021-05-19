import os
from datetime import datetime
import logging
from typing import Optional, Any
from enum import Enum

from pydantic import BaseModel

class Status(Enum):
    DEFAULT = 0

    REQUEST_EMPTY_ONCE = 11
    REQUEST_DOING = 20
    REQUEST_DONE = 21

    GENERATE_FAILED = 22
    GENERATE_DONE = 30

    DOWNLOAD_FAILED = 31
    DOWNLOAD_DONE = 40

    RENAME_FAILED = 41
    RENAME_DONE = 50

    UPLOAD_FAILED = 51
    UPLOAD_DONE = 60

    ERASE_FAILED = 61
    ERASE_DONE = 70

    ALL_DONE = 80
    REQUEST_EMPTY_TWICE = 81

    def __ge__(self, other):
        if self.__class__ is other.__class__:
            return self.value >= other.value
        return NotImplemented
    def __gt__(self, other):
        if self.__class__ is other.__class__:
            return self.value > other.value
        return NotImplemented
    def __le__(self, other):
        if self.__class__ is other.__class__:
            return self.value <= other.value
        return NotImplemented
    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented

class EventHelper(BaseModel):
    timestamp: Optional[datetime]
    status: Optional[Status] = Status.DEFAULT

    def __repr__(self):
        return f'{self.timestamp} | {self.status}'

    def __str__(self):
        return f'{self.timestamp} | {self.status}'