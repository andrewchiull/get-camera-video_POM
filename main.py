import os
from datetime import datetime, timedelta
import logging

from selenium import webdriver

from spotcam_utils.directory_helper import DirectoryHelper

from spotcam_utils.pages.login_page_actions import LoginPage


def main():
    CAMERA_PLACE = 'Chiayi'

    yesterday = datetime.now() + timedelta(days=-1)
    DATE = yesterday

    format_str = '%(asctime)s %(levelname)s | %(message)s'
    logging_level = logging.INFO

    logging.basicConfig(
        format=format_str, 
        level=logging_level
        )


    dirh = DirectoryHelper(DATE, CAMERA_PLACE)

if __name__ == "__main__":
    main()