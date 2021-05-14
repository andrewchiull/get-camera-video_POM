import os
import sys
from datetime import datetime, timedelta
import logging

import ipdb

from selenium import webdriver

from spotcam_utils.directory_helper import DirectoryHelper
from spotcam_utils.pages.login_page_actions import LoginPage
from spotcam_utils.config_helper import ConfigHelper

CAMERA_PLACE = 'Chiayi'

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

    driver = init_driver()

    login_page = LoginPage(driver)
    login_page.get_login_page()
    login_page.input_username(config.get_username())
    login_page.input_password(config.get_password())
    login_page.click_login_button()
    
    ipdb.set_trace() # IPDB


def init_driver():
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

if __name__ == "__main__":
    main()