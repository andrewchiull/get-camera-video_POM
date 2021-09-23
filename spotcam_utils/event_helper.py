import os
from datetime import datetime
from typing import Optional
from enum import Enum

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

class EventHelper():
    def __init__(self,
        timestamp: Optional[datetime],
        status: Optional[Status] = Status.DEFAULT) -> None:

        self.timestamp = timestamp
        self.status = status

    def __repr__(self) -> str:
        return f'{self.timestamp} | {self.status}'