import time
import logging
from datetime import datetime
from typing import Optional

from spotcam_utils.base_page import BasePage
from spotcam_utils.pages.camera_page_locators import CameraPageLocators
from spotcam_utils.event_helper import Status

import ipdb


class CameraPage(BasePage):

    _locators = CameraPageLocators()

    def __init__(self, driver, date):
        super().__init__(driver)
        self.date: Optional[datetime] = date

    def get_camera_page(self, camera_name: str):
        url = 'https://www.myspotcam.com/tc/myspotcam/'
        self.get_page(url)
        self.click_element(self._locators.CAMERA_PAGE(camera_name))
        self.click_element(self._locators.PAUSE_BTN)
        self.remove_element(self.find_element(self._locators.STREAM))

    def check_month_and_year_on_calendar(self) -> bool:
        self.click_element(self._locators.CALENDAR_BOX)
        self.wait_page_until_loading()
        month_year_expect = self.date.strftime('%B , %Y')
        CHECK_TIMES = 3

        for _ in range(CHECK_TIMES):
            month_year_actual = self.find_element(
                    self._locators.DATE_TITLE).get_attribute("innerText")

            if month_year_expect == month_year_actual:
                return True
            else:
                logging.info(f'Click last month.')
                self.click_element(self._locators.PREVIOUS_MONTH)
                self.wait_page_until_loading()


        return False

    def check_day_on_calendar(self):
        date_on_calendar = self.find_element(self._locators.DATE_ON_CALENDAR(date=self.date))

        if 'disabled' in date_on_calendar.get_attribute("class"):
            return False
        self.click_element(self._locators.DATE_ON_CALENDAR(date=self.date))
        return True

    def get_motion_events(self) -> list:
        self.click_element(self._locators.EVENT_LIST)
        self.wait_page_until_loading()
        self.click_element(self._locators.SLIDE_OF_EVENT_LIST)
        self.wait_page_until_loading()
        self.click_element(self._locators.MOTION_EVENT_LIST)
        self.wait_page_until_loading()
        motion_events = self.find_elements(self._locators.MOTION_EVENT)
        motion_events.reverse()
        return motion_events

    def request_video(self, timestamp: datetime):
        self.click_element(self._locators.REQUEST_VIDEOS)
        self.wait_page_until_loading()
        options = {
            'year': timestamp.strftime('%Y'),
            'month': timestamp.strftime('%m'),
            'date': timestamp.strftime('%d'),
            'hour': timestamp.strftime('%H'),
            'minute': timestamp.strftime('%M')
        }
        for time_scale, value in options.items():
            self.select(self._locators.OPTION(time_scale), value)
            expected_value = self.find_element(self._locators.RESULT(time_scale)).get_attribute('innerText')
            assert value == expected_value, f'{value = }, {expected_value = }'

        # Generate a 2 min video in case the alert happens in the end of 1 min video.
        if timestamp.second > 50:
            logging.info('Generate a 2 min video.')
            video_length = '2'
        else:
            logging.info('Generate a 1 min video.')
            video_length = '1'
        self.select(self._locators.OPTION_LENGTH, video_length)
        expected_video_length = self.find_element(self._locators.RESULT_LENGTH).get_attribute('innerText')
        assert video_length == expected_video_length, f'{video_length = }, {expected_video_length = }'

        self.click_element(self._locators.OK_BTN)
        self.wait_page_until_loading()

    def read_alert_message(self, status_old) -> Status:
        message = self.find_element(
            self._locators.ALERT_BOX).get_attribute('innerText')
        logging.info(f'Alert message: {message}')
        self.click_element(self._locators.ACCEPT_BTN)
        self.wait_page_until_loading()

        if message == '您的影片正在製作中，製作完成後將會顯示在您的「我的影片」頁面中。':
            logging.info(f'影片已要求。')
            return Status.REQUEST_DONE

        elif message == '目前有一個影片正在製作中，請先等待目前影片製作完成。':
            logging.info(f'影片要求中。')
            return Status.REQUEST_DOING

        elif message == '您選取的時間區間內並沒有錄影檔' and status_old == Status.DEFAULT:
            logging.info(f'此時段沒有錄到影，跳過此影片。（第一次）')
            return Status.REQUEST_EMPTY_ONCE

        elif message == '您選取的時間區間內並沒有錄影檔' and status_old == Status.REQUEST_EMPTY_ONCE:
            logging.info(f'此時段沒有錄到影，跳過此影片。（第二次）')
            return Status.REQUEST_EMPTY_TWICE

        else:
            logging.info(f'Unknown Error')
            return Status.DEFAULT