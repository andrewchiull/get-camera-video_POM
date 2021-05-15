import os
from datetime import datetime
import logging
from typing import Optional, Any

from pydantic import BaseModel

class DirectoryHelper(BaseModel):

    DATE: Optional[datetime]
    CAMERA_PLACE: str
    HOME = os.environ['HOME']
    PWD = os.environ['PWD']
    DRIVER: str = ''
    DOWNLOADS: str = ''
    UNRENAMED: str = ''
    RENAMED: str = ''


    def __init__(self, **data: Any):
        super().__init__(**data)
        self.DRIVER = os.path.join(self.PWD, 'spotcam_utils/browser_driver')

        self.DOWNLOADS = os.path.join(self.HOME, 'Downloads')
        if not os.path.exists(self.DOWNLOADS):
            os.mkdir(self.DOWNLOADS)
            logging.info(f'mkdir: {self.DOWNLOADS}')

        self.UNRENAMED = os.path.join(self.DOWNLOADS, 'unrenamed')
        if not os.path.exists(self.UNRENAMED):
            os.mkdir(self.UNRENAMED)
            logging.info(f'mkdir: {self.UNRENAMED}')

        date_str = self.DATE.strftime('%Y-%m-%d')
        self.RENAMED = os.path.join(
            self.DOWNLOADS, f'{self.CAMERA_PLACE}_{date_str}')
        if not os.path.exists(self.RENAMED):
            os.mkdir(self.RENAMED)
            logging.info(f'mkdir: {self.RENAMED}')

