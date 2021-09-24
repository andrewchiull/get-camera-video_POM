import os
import sys
from datetime import datetime
import logging
import shutil

from spotcam_utils.config_helper import ConfigHelper

class DirectoryHelper():
    def __init__(self, CAMERA_NAME, DATE = datetime.now()):
        self.CAMERA_NAME = CAMERA_NAME
        self.DATE = DATE
        self.HOME = os.environ['HOME']
        self.PWD = os.environ['PWD']
        self.os = {
            'darwin': 'macos',
            'linux': 'linux'
        }
        self.DRIVER = os.path.join(
            self.PWD, 'spotcam_utils/browser_driver', self.os[sys.platform])

        self.DOWNLOADS = os.path.join(self.HOME, 'Downloads')
        if not os.path.exists(self.DOWNLOADS):
            os.mkdir(self.DOWNLOADS)
            logging.info(f'mkdir: {self.DOWNLOADS}')

        self.UNRENAMED = os.path.join(self.DOWNLOADS, 'unrenamed')
        # Reset UNRENAMED everyday
        if os.path.exists(self.UNRENAMED):
            shutil.rmtree('/folder_name')
        if not os.path.exists(self.UNRENAMED):
            os.mkdir(self.UNRENAMED)
            logging.info(f'mkdir: {self.UNRENAMED}')

        date_str = self.DATE.strftime('%Y-%m-%d')
        self.RENAMED = os.path.join(
            self.DOWNLOADS, f'{self.CAMERA_NAME}_{date_str}')
        if not os.path.exists(self.RENAMED):
            os.mkdir(self.RENAMED)
            logging.info(f'mkdir: {self.RENAMED}')

        config = ConfigHelper(os.path.join(self.PWD, 'config.yaml'))
        self.FTP = {
            'BIME-YunLin': os.path.join(config.get_FTPDIR(), '雲林斗六'),
            'BIME-ChiaYi': os.path.join(config.get_FTPDIR(), '嘉義太保')
        }
