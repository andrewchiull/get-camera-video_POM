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

# CAMERA_PLACE = 'Chiayi'
CAMERA_PLACE = 'Yunlin'

yesterday = datetime.now() + timedelta(days=-1)
DATE = yesterday
logging.basicConfig(
    format='%(asctime)s %(levelname)s | %(message)s', 
    level=logging.INFO,
    # level=logging.DEBUG
    )

dirs_data = {'DATE': DATE, 'CAMERA_PLACE': CAMERA_PLACE}
dirs = DirectoryHelper(**dirs_data)

config_path = os.path.join(dirs.PWD, 'config.yaml')
config = ConfigHelper(config_path)

def main():
    driver = get_driver()
    login(driver)
    events = get_events(driver)
    logging.info('\n' + pformat(events))
    if not events:
        driver.quit()
        return


    ipdb.set_trace() # IPDB

def get_driver():
    options = webdriver.ChromeOptions()
    prefs = {
        'profile.default_content_setting_values': {
            'notifications': 2
        },
        'download.default_directory': dirs.UNRENAMED
    }
    options.add_experimental_option('prefs', prefs)
    options.add_argument('--start-fullscreen')
    # options.headless = True # TEST headless mode

    sys.path.append(dirs.DRIVER)
    driver_path = os.path.join(dirs.DRIVER, 'chromedriver')
    driver = webdriver.Chrome(driver_path, options=options)
    return driver

def login(driver):
    login_page = LoginPage(driver)
    login_page.get_login_page()
    login_page.input_username(config.get_username())
    login_page.input_password(config.get_password())
    login_page.click_login_button()

def get_events(driver) -> Dict[int, EventHelper]:
    events = {}
    camera_page = CameraPage(driver)
    camera_page.get_camera_page(dirs.CAMERA_PLACE)
    date_on_calendar = camera_page.get_date_on_calendar(DATE)
    logging.info(date_on_calendar.get_attribute("class"))
    logging.info('The day of the date is:')
    logging.info(date_on_calendar.get_attribute("innerText"))
    if 'disabled' in date_on_calendar.get_attribute("class"):
        logging.warning('There are no events on the date.')
        return events
    date_on_calendar.click()

    motion_events = camera_page.get_motion_events()
    if not motion_events:
        logging.warning('There are no motion events on the date.')
        return events
    
    for index, ev in enumerate(motion_events):
        ev_text = ev.get_attribute('innerText')[4:]
        ev_time = datetime.strptime(ev_text, "\n\n%Y/%m/%d\n\n%H:%M:%S")
        events[index] = EventHelper(**{'time':ev_time})

    return events

"""

4. Return a dict of objects:

   - TODO Refine this.
   - Export this as yaml (or json)?

   ```
   events = {
      0: {
         time: datetime,
        requested: bool = False
        empty_once: bool = False
        empty_twice: bool = False

        generated: bool = False
        downloaded: bool = False
        renamed: bool = False
        uploaded: bool = False
        erased: bool = False
      },
      1: ...
   }
   ```
"""

if __name__ == "__main__":
    main()