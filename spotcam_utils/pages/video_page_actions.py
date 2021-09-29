import os
import time
import logging
from datetime import datetime
from typing import Optional
import shutil

from spotcam_utils.base_page import BasePage
from spotcam_utils.pages.video_page_locators import VideoPageLocators
from spotcam_utils.event_helper import Status
from spotcam_utils.directory_helper import DirectoryHelper
from spotcam_utils.ftp_helper import FtpHelper

import ipdb


class VideoPage(BasePage):

    _locators = VideoPageLocators()

    def __init__(self, driver, dirs, config, camera_name):
        super().__init__(driver)
        self.dirs: DirectoryHelper = dirs
        self.ftp = FtpHelper(config)
        self.camera_name = camera_name

    def get_video_page(self):
        url = 'https://www.myspotcam.com/tc/myspotcam/myfilm'
        self.get_page(url)
        # Remove the element(addSpotcam) that could block clicking
        self.remove_element(self.find_element(self._locators.ADD_SPOTCAM))

    def get_generated_videos(self) -> list:
        videos = self.find_elements(self._locators.GENERATED_VIDEOS)
        generated_videos = (
            [datetime.strptime(video.get_attribute('innerText'), "%m/%d/%Y\nat %H:%M:%S")
             for video in videos])
        return generated_videos

    def download_video(self, timestamp_generated: datetime):
        date_str = datetime.strftime(timestamp_generated, "%m/%d/%Y")
        time_str = datetime.strftime(timestamp_generated, "%H:%M:%S")
        self.box = f'//*[text()[contains(.,"{date_str}")]][text()[contains(.,"{time_str}")]]/..'

        self.click_element(self._locators.LINK(self.box, self.camera_name))
        self.click_element(self._locators.PLAY)
        self.click_element(self._locators.PAUSE)
        self.click_element(self._locators.DOWNLOAD)

    def is_video_downloaded(self) -> bool:
        RETRY_TIMES = 10
        for _ in range(RETRY_TIMES):
            time.sleep(1)
            all_mp4 = [f for f in os.listdir(self.dirs.UNRENAMED)
                     if ('mp4' in f) and ('crdownload' not in f)]
            if len(all_mp4) == 1:
                self.video_original_name = all_mp4[0]
                logging.info(f'Original name of video: {self.video_original_name}')
                return True
            elif len(all_mp4) > 1:
                logging.error(f'More than one video is in unrenamed: {all_mp4}')
                shutil.rmtree(self.dirs.UNRENAMED)
                os.mkdir(self.dirs.UNRENAMED)
                logging.error(f'Clear all videos in unrenamed')

        return False

    def rename_video(self, key: int, timestamp: datetime):
        path_unrenamed = os.path.join(self.dirs.UNRENAMED, self.video_original_name)
        time_str = timestamp.strftime('%Y-%m-%d_%H-%M-%S')

        self.video_full_name = f'{self.camera_name}_{time_str}_{key:02}.mp4'
        logging.info(f'New full name of video: {self.video_full_name}')
        self.path_renamed = os.path.join(self.dirs.RENAMED, self.video_full_name)
        shutil.move(path_unrenamed, self.path_renamed)

    def upload_video(self):
        upload_path = os.path.join(self.dirs.FTP[self.camera_name], self.video_full_name)
        self.ftp.upload(self.path_renamed, upload_path)

    def erase_video(self):
        url = 'https://www.myspotcam.com/tc/myspotcam/myfilm'
        self.get_page(url)
        self.find_element(self._locators.ERASE(self.box)).click()
        self.wait_and_accept_alert()

    def is_video_renamed(self, key: int, timestamp: datetime):
        time_str = timestamp.strftime('%Y-%m-%d_%H-%M-%S')
        video_full_name = f'{self.camera_name}_{time_str}_{key:02}.mp4'
        path_renamed = os.path.join(self.dirs.RENAMED, video_full_name)
        return os.path.exists(path_renamed)

    def upload_txt(self, txt_path, txt_name):
        upload_path = os.path.join(self.dirs.FTP[self.camera_name], txt_name)
        self.ftp.upload(txt_path, upload_path)