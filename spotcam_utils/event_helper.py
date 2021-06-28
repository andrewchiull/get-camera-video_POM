import os
from datetime import datetime
import logging
from typing import Optional, Any
from enum import Enum

from pydantic import BaseModel

class Status(Enum):
    DEFAULT = 0

    REQUEST_EMPTY_ONCE = 11
    GENERATE_FAILED = 19

    REQUEST_DOING = 20
    REQUEST_DONE = 21

    GENERATE_DONE = 30

    DOWNLOAD_FAILED = 31
    DOWNLOAD_DONE = 40

    ALL_DONE = 100
    REQUEST_EMPTY_TWICE = 102

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

    # def __repr__(self):
    #     return f'{self.timestamp} | {self.status}'

    def __str__(self):
        return f'{self.timestamp} | {self.status}'