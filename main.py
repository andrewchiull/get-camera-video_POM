import os
import sys
from datetime import datetime, timedelta
import logging
from typing import Dict

import ipdb

from selenium import webdriver

from spotcam_utils.directory_helper import DirectoryHelper
from spotcam_utils.pages.login_page_actions import LoginPage
from spotcam_utils.pages.camera_page_actions import CameraPage
from spotcam_utils.config_helper import ConfigHelper
from spotcam_utils.event_helper import EventHelper
from pprint import pprint, pformat

class Main:
    def __init__(self):
        # self.CAMERA_PLACE = 'Chiayi'
        self.CAMERA_PLACE = 'Yunlin'
        self.DATE = datetime.now() + timedelta(days=-1)
        # self.DATE = self.DATE.replace(year=2021, month=4, day=30)
        self.dirs = DirectoryHelper(**{'DATE': self.DATE, 'CAMERA_PLACE': self.CAMERA_PLACE})
        self.config = ConfigHelper(os.path.join(self.dirs.PWD, 'config.yaml'))

    def main(self):
        self.driver = self.get_driver()
        self.login(self.driver, self.config)
        self.events = self.get_events(self.driver, self.DATE, self.dirs)
        logging.info('\n' + pformat(self.events))
        if not self.events:
            logging.warning('There are no events on the date.')
            logging.warning('Driver quits.')
            self.driver.quit()
            return


        ipdb.set_trace() # IPDB

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
        # options.headless = True # TEST headless mode

        sys.path.append(self.dirs.DRIVER)
        driver_path = os.path.join(self.dirs.DRIVER, 'chromedriver')
        driver = webdriver.Chrome(driver_path, options=options)
        driver.set_window_size(1024, 768)
        # driver.maximize_window()
        return driver

    def login(self, driver, config):
        login_page = LoginPage(driver)
        login_page.get_login_page()
        login_page.input_username(config.get_username())
        login_page.input_password(config.get_password())
        login_page.click_login_button()

    def get_events(self, driver, date, dirs) -> Dict[int, EventHelper]:
        camera_page = CameraPage(driver, date)
        camera_page.get_camera_page(dirs.CAMERA_PLACE)
        if not camera_page.check_month_and_year_on_calendar():
            logging.warning('The date is too long ago from now.')
            return {}
        if not camera_page.check_day_on_calendar():
            logging.warning('There are not any kinds of events on the date.')
            return {}

        motion_events = camera_page.get_motion_events()
        if not motion_events:
            logging.warning('There are no motion events on the date.')
            return {}
        
        events = {}
        for index, ev in enumerate(motion_events):
            ev_text = ev.get_attribute('innerText')[4:]
            ev_time = datetime.strptime(ev_text, "\n\n%Y/%m/%d\n\n%H:%M:%S")
            events[index] = EventHelper(**{'time':ev_time})

        return events

"""

4. Return a dict of objects:

"""

def main():
    m = Main()
    m.main()

if __name__ == "__main__":
    logging.basicConfig(
        format='%(asctime)s %(levelname)s | %(message)s', 
        level=logging.INFO,
        # level=logging.DEBUG
        )

    main()