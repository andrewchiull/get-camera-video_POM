import os
import sys
from datetime import datetime
import logging
from typing import Optional, Any

from pydantic import BaseSettings

from spotcam_utils.config_helper import ConfigHelper


class DirectoryHelper(BaseSettings):
    CAMERA_NAME: str
    DATE: Optional[datetime] = datetime.now()

    # BaseSettings determines the values by reading from the environment
    HOME: str
    PWD: str

    DRIVER: str = ''
    DOWNLOADS: str = ''
    UNRENAMED: str = ''
    RENAMED: str = ''
    FTP: dict = {}
    os = {
        'darwin': 'macos',
        'linux': 'linux'
    }
    config = None
    def __init__(self, **data: Any):
        super().__init__(**data)

        self.DRIVER = os.path.join(
            self.PWD, 'spotcam_utils/browser_driver', self.os[sys.platform])

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
            self.DOWNLOADS, f'{self.CAMERA_NAME}_{date_str}')
        if not os.path.exists(self.RENAMED):
            os.mkdir(self.RENAMED)
            logging.info(f'mkdir: {self.RENAMED}')

        self.config = ConfigHelper(os.path.join(self.PWD, 'config.yaml'))
        self.FTP = {
            'BIME-YunLin': os.path.join(self.config.get_FTPDIR(), '雲林斗六'),
            'BIME-ChiaYi': os.path.join(self.config.get_FTPDIR(), '嘉義太保')
        }
