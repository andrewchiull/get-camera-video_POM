import time
import logging
from datetime import datetime

from spotcam_utils.base_page import BasePage
from spotcam_utils.pages.camera_page_locators import CameraPageLocators

import ipdb

class CameraPage(BasePage):

    _locators = CameraPageLocators()

    def get_camera_page(self, camera_place):
        url = 'https://www.myspotcam.com/tc/myspotcam/'
        self.get_page(url)
        self.click_element(self._locators.CAMERA_PAGE[camera_place])
        self.wait_page_until_loading()
        self.remove_element(self.find_element(self._locators.STREAM))
        self.click_element(self._locators.PAUSE_BTN)
    
    def get_date_on_calendar(self, date: datetime):
        self.click_element(self._locators.CALENDAR_BOX)
        dateTitle_expect = date.strftime('%B , %Y')
        dateTitle_actual = \
            self.find_element(self._locators.DATE_TITLE).get_attribute("innerText")

        logging.info(f'dateTitle_expect = {dateTitle_expect}')
        logging.info(f'dateTitle_actual = {dateTitle_actual}')
        while dateTitle_expect != dateTitle_actual:
            self.click_element(self._locators.PREVIOUS_MONTH)
            logging.info(f'Click last month.')
            dateTitle_actual = \
                self.find_element(self._locators.DATE_TITLE).get_attribute("innerText")
            logging.info(f'dateTitle_actual = {dateTitle_actual}')
        logging.info(f'(dateTitle_expect == dateTitle_actual) = {(dateTitle_expect == dateTitle_actual)}')

        date_on_calendar = \
            self.find_element(self._locators.DATE_ON_CALENDAR(date=date))
        return date_on_calendar

    def get_motion_events(self) -> list:
        self.click_element(self._locators.EVENT_LIST)
        self.click_element(self._locators.SLIDE_OF_EVENT_LIST)
        self.click_element(self._locators.MOTION_EVENT_LIST)
        motion_events = self.find_elements(self._locators.MOTION_EVENT)
        motion_events.reverse()
        return motion_events


