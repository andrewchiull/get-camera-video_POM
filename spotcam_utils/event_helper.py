import os
from datetime import datetime
import logging
from typing import Optional, Any

from pydantic import BaseModel

class EventHelper(BaseModel):

    time: Optional[datetime]
    requested: bool = False
    empty_once: bool = False
    empty_twice: bool = False

    generated: bool = False
    downloaded: bool = False
    renamed: bool = False
    uploaded: bool = False
    erased: bool = False

