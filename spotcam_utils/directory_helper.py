import os
from datetime import datetime
import logging
from typing import Optional

from pydantic.dataclasses import dataclass

@dataclass
class DirectoryHelper():

    DATE: Optional[datetime]
    CAMERA_PLACE: str
    HOME = os.environ['HOME']
    # PWD = os.environ['PWD']

    def __post_init__(self):

        self.downloads = os.path.join(self.HOME, 'Downloads')
        if not os.path.exists(self.downloads):
            os.mkdir(self.downloads)
            logging.info(f'mkdir: {self.downloads}')

        self.UNRENAMED_DIR = os.path.join(self.downloads, 'unrenamed')
        if not os.path.exists(self.UNRENAMED_DIR):
            os.mkdir(self.UNRENAMED_DIR)
            logging.info(f'mkdir: {self.UNRENAMED_DIR}')

        date_str = self.DATE.strftime('%Y-%m-%d')
        self.RENAMED_DIR = os.path.join(
            self.downloads, f'{self.CAMERA_PLACE}_{date_str}')
        if not os.path.exists(self.RENAMED_DIR):
            os.mkdir(self.RENAMED_DIR)
            logging.info(f'mkdir: {self.RENAMED_DIR}')

