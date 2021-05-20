from selenium.webdriver.common.by import By
from datetime import datetime


class CameraPageLocators:
    # locators
    
    STREAM = (By.XPATH, '//*[@class="divide divide1 active"]')
    PAUSE_BTN = (By.XPATH, '//*[@class="controlBtn pauseBtn"]')
    CALENDAR_BOX = (By.XPATH, '//*[@class="calendarBox"]')
    DATE_TITLE = (By.XPATH, '//*[@class="dateTitle"]')
    PREVIOUS_MONTH = (By.XPATH, '//*[@class="calendarBtn prev"]')
    EVENT_LIST = (By.XPATH, '//*[@class="icon iconEvent"]')
    SLIDE_OF_EVENT_LIST = (By.XPATH, '//*[@class="slideEventListBtn"]')
    MOTION_EVENT_LIST = (By.XPATH, '//*[@class="senseFilter motionBtn"]')
    MOTION_EVENT = (By.XPATH, '//*[@class="event motion_filter"]')

    REQUEST_VIDEOS = (By.XPATH, '//a[@data-text="filmBtnText"]')
    OPTION_LENGTH = (By.XPATH, '//*[@id="export_length"]')
    RESULT_LENGTH = (By.XPATH, '//*[@id="export_length"]/../*[@class="select-label"]')
    OK_BTN = (By.XPATH, '//a[@tkey="ok_btn"]')

    ALERT_BOX = (By.XPATH, '//*[@id="alertCustomised"]//*[@class="alert-box"]/p')
    ACCEPT_BTN = (By.XPATH, '//*[@id="alertCustomised"]//*[@class="btn btn-blue btnClose"]')

    def CAMERA_PAGE(self, camera_name):
        return (By.XPATH, f'//a[@title="{camera_name}"]')

    def DATE_ON_CALENDAR(self, date: datetime):
        return (By.XPATH, f'//*[@id="days"]/li/span[text()="{date.day}"]/..')
    
    def OPTION(self, option):
        return (By.XPATH, f'//*[@id="export_select_{option}"]')
    
    def RESULT(self, option):
        return (By.XPATH, f'//*[@id="select_export_{option}"]')

