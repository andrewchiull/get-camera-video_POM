# -*- coding: utf-8 -*-
"""
Created on 2021/03/30
@author: Jim
"""
import ftplib
import os
import time
from datetime import datetime
import logging

from spotcam_utils.config_helper import ConfigHelper


class FtpHelper():

    def __init__(self, config: ConfigHelper):
        self.ftp = ftplib.FTP()
        self.ftp.encoding = 'big5'

        FTPIP = config.get_FTPIP()
        FTPPORT = config.get_FTPPORT()
        USERNAME = config.get_USERNAME()
        USERPWD = config.get_USERPWD()
        self.ftp.connect(FTPIP, FTPPORT)
        self.ftp.login(USERNAME, USERPWD)
        logging.info("[FTP] Login...")
        logging.info(self.ftp.getwelcome())

    def upload(self, local_path, remote_path):
        bufsize = 1024
        file_handler = open(local_path, 'rb')  # local file
        STOR = f'STOR {remote_path}'
        self.ftp.storbinary(STOR, file_handler, bufsize)
        self.ftp.set_debuglevel(0)
        file_handler.close()
