from selenium.webdriver.common.by import By
from datetime import datetime


class CameraPageLocators:
    # locators
    CAMERA_PAGE = {
        'Chiayi': (By.XPATH, f'//a[@title="BIME-ChiaYi"]'),
        'Yunlin': (By.XPATH, f'//a[@title="BIME-YunLin"]')
    }
    STREAM = (By.XPATH, '//*[@class="divide divide1 active"]')
    PAUSE_BTN = (By.XPATH, '//*[@class="controlBtn pauseBtn"]')
    CALENDAR_BOX = (By.XPATH, '//*[@class="calendarBox"]')
    DATE_TITLE = (By.XPATH, '//*[@class="dateTitle"]')
    PREVIOUS_MONTH = (By.XPATH, '//*[@class="calendarBtn prev"]')
    EVENT_LIST = (By.XPATH, '//*[@class="icon iconEvent"]')
    SLIDE_OF_EVENT_LIST = (By.XPATH, '//*[@class="slideEventListBtn"]')
    MOTION_EVENT_LIST = (By.XPATH, '//*[@class="senseFilter motionBtn"]')
    MOTION_EVENT = (By.XPATH, '//*[@class="event motion_filter"]')
    
    def DATE_ON_CALENDAR(self, date: datetime):
        return (By.XPATH, f'//*[@id="days"]/li/span[text()="{date.day}"]/..')

