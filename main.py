import os
import sys
from datetime import datetime, timedelta
import logging
import traceback
from typing import Dict
from pprint import pprint, pformat

import ipdb

from selenium import webdriver

from spotcam_utils.directory_helper import DirectoryHelper
from spotcam_utils.config_helper import ConfigHelper
from spotcam_utils.event_helper import EventHelper
from spotcam_utils.event_helper import Status
from spotcam_utils.pages.login_page_actions import LoginPage
from spotcam_utils.pages.camera_page_actions import CameraPage
from spotcam_utils.pages.video_page_actions import VideoPage


class Main:
    def __init__(self, date, location):
        # self.LOCATION = 'Chiayi' or 'Yunlin'
        self.LOCATION: str = location
        self.CAMERA_NAME = {
            'Yunlin': 'BIME-YunLin',
            'Chiayi': 'BIME-ChiaYi'
        }
        self.DATE = date
        # self.DATE = self.DATE.replace(year=2021, month=6, day=30 # TEST given date
        self.dirs = DirectoryHelper(
            DATE=self.DATE, CAMERA_NAME=self.CAMERA_NAME[self.LOCATION])
        self.config = ConfigHelper(os.path.join(self.dirs.PWD, 'config.yaml'))
        self.ERR_COUNT = 0

    def main(self):
        RETRY_TIMES = 3
        for i in range(RETRY_TIMES):
            try:
                logging.info('')
                self.log_title('')

                self.log_title(f'Get videos from {self.CAMERA_NAME[self.LOCATION]}')
                self.log_title(f'{self.DATE.date()}')
                self.driver = self.get_driver()

                self.log_title(f'Login')
                self.login()

                self.log_title(f'Get events')
                self.events = self.get_events()
                if self.events is None:
                    logging.warning('There are no events on the date. Driver quits.')
                    return
                logging.info('\n' + pformat(self.events))

                self.log_title(f'Check videos whose request is skippable')
                self.check_is_skippable()
                break
            except Exception:
                self.error_message()
                continue


        RETRY_TIMES = 10
        for i in range(RETRY_TIMES):
            try:
                self.log_title(f'Round {i}: Requesting')
                self.request_videos() # TEST_NORMAL_OPEN skip request
                logging.info('\n' + pformat(self.events))

                self.log_title(f'Round {i}: Downloading')
                self.download_videos()
                logging.info('\n' + pformat(self.events))
            except Exception:
                self.error_message()
                continue
            if all(event.status >= Status.ALL_DONE for event in self.events.values()):
                self.log_title('Whole process finished')
                self.log_title('')
                logging.info('')
                return

    def get_driver(self):
        options = webdriver.ChromeOptions()
        prefs = {
            'profile.default_content_setting_values': {
                'notifications': 2
            },
            'download.default_directory': self.dirs.UNRENAMED
        }
        options.add_experimental_option('prefs', prefs)
        # options.add_argument('--start-fullscreen')
        # options.headless = True # TEST_NORMAL_OPEN headless mode

        sys.path.append(self.dirs.DRIVER)
        driver_path = os.path.join(self.dirs.DRIVER, 'chromedriver')
        driver = webdriver.Chrome(driver_path, options=options)
        driver.set_window_size(1024, 768)
        # driver.maximize_window()
        return driver

    def login(self):
        login_page = LoginPage(self.driver)
        login_page.get_login_page()
        login_page.input_username(self.config.get_username())
        login_page.input_password(self.config.get_password())
        login_page.click_login_button()

    def get_events(self) -> Dict[int, EventHelper]:
        camera_page = CameraPage(self.driver, self.DATE)
        camera_page.get_camera_page(self.CAMERA_NAME[self.LOCATION])
        if not camera_page.check_month_and_year_on_calendar():
            logging.warning('The date is too long ago from now.')
            return
        if not camera_page.check_day_on_calendar():
            logging.warning('There are not any kinds of events on the date.')
            return

        motion_events = camera_page.get_motion_events()
        if not motion_events:
            logging.warning('There are no motion events on the date.')
            return

        # motion_events = motion_events[:3]  # TEST Use some events

        events = {}
        for index, ev in enumerate(motion_events):
            ev_text = ev.get_attribute('innerText')[4:]
            ev_time = datetime.strptime(ev_text, "\n\n%Y/%m/%d\n\n%H:%M:%S")
            events[index] = EventHelper(timestamp=ev_time)

        return events

    def check_is_skippable(self):
        video_page = VideoPage(
            self.driver, self.dirs, self.config, self.CAMERA_NAME[self.LOCATION])
        logging.info('')
        for key, ev in self.events.items():
            if video_page.is_video_renamed(key, ev.timestamp):
                ev.status = Status.ALL_DONE
                self.log_status(key)
                continue

            video_page.get_video_page()
            # "second" of videos in generated_videos is 00
            timestamp_generated = ev.timestamp.replace(second=0)
            if timestamp_generated in video_page.get_generated_videos():
                ev.status = Status.GENERATE_DONE
                self.log_status(key)
                continue  # Skip the ungenerated events

            self.log_status(key)
        logging.info('')

    def request_videos(self):
        camera_page = CameraPage(self.driver, self.DATE)
        camera_page.get_camera_page(self.CAMERA_NAME[self.LOCATION])
        for key, ev in self.events.items():
            self.log_status(key)
            if ev.status >= Status.REQUEST_DONE:
                continue  # Skip the requested events
            camera_page.request_video(ev.timestamp)
            ev.status = camera_page.read_alert_message(ev.status)
            self.log_status(key)
            logging.info('')

    def download_videos(self):
        video_page = VideoPage(
            self.driver, self.dirs, self.config, self.CAMERA_NAME[self.LOCATION])

        # Make a txt containing all events
        date_str = self.DATE.strftime('%Y-%m-%d')
        events_txt_filename = f'{self.CAMERA_NAME[self.LOCATION]}_{date_str}.txt'
        events_txt_path = os.path.join(self.dirs.RENAMED, events_txt_filename)
        f = open(events_txt_path, 'w')
        for key, ev in self.events.items():
            time_str = ev.timestamp.strftime('%Y-%m-%d_%H-%M-%S')
            f.write(f'{self.CAMERA_NAME[self.LOCATION]}_{time_str}_{key:02}.mp4')
            f.write('\n')
        f.close()
        video_page.upload_txt(events_txt_path, events_txt_filename)

        for key, ev in self.events.items():
            self.log_status(key)
            if ev.status >= Status.ALL_DONE or ev.status == Status.REQUEST_EMPTY_ONCE:
                continue  # Skip the completed or empty events

            video_page.get_video_page()

            # "second" of videos in generated_videos is 00
            timestamp_generated = ev.timestamp.replace(second=0)

            if timestamp_generated not in video_page.get_generated_videos():
                ev.status = Status.GENERATE_FAILED
                self.log_status(key)
                continue  # Skip the ungenerated events

            video_page.download_video(timestamp_generated)

            if video_page.is_video_downloaded():
                ev.status = Status.DOWNLOAD_DONE
                self.log_status(key)
            else:
                ev.status = Status.DOWNLOAD_FAILED
                self.log_status(key)
                continue

            video_page.rename_video(key, ev.timestamp)
            video_page.upload_video()
            video_page.erase_video()

            ev.status = Status.ALL_DONE
            self.log_status(key)
            logging.info('')

    def log_title(self, msg, level=logging.INFO):
        msg = f'[ {msg} ]'
        logging.log(msg=f'{msg:=^60}', level=level)

    def error_message(self):
        err_head = f'ERROR #{self.ERR_COUNT: >2}'
        err_msg = traceback.format_exc()
        err_tail = f'END   #{self.ERR_COUNT: >2}'
        self.log_title(err_head, logging.ERROR)
        logging.error(f'\n{err_msg}\n')
        self.log_title(err_tail, logging.ERROR)
        self.ERR_COUNT += 1

    def log_status(self, key):
        logging.info(f'{key: >2}: {self.events[key]}')


def main():
    date = datetime.now() - timedelta(days=1)
    Yunlin = Main(date=date, location='Yunlin')
    Yunlin.main()
    Yunlin.driver.quit()

    Chiayi = Main(date=date, location='Chiayi')
    Chiayi.main()
    Chiayi.driver.quit()

if __name__ == "__main__":
    logging.basicConfig(
        format='%(asctime)s %(levelname)s | %(message)s',
        level=logging.INFO
    )

    main()
