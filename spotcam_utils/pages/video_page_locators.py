from selenium.webdriver.common.by import By
from datetime import datetime


class VideoPageLocators:
    # locators
    ADD_SPOTCAM = (By.XPATH, '//*[@class="addSpotcam"]')
    GENERATED_VIDEOS = (By.XPATH, '//*[@class="upmodename"]')

    # PLAY = (By.XPATH, '//*[contains(@class,"vjs-big-play-button")]')
    PLAY = (By.XPATH, '//*[@class="vjs-big-play-button"]')
    PAUSE = (By.XPATH, '//*[@aria-label="Video Player"]')
    DOWNLOAD = (By.XPATH, '//*[@class="vjs-control vjs-download-button"]')

    def LINK(self, box, camera_name):
        return (By.XPATH, f'{box}/.//*[text()[contains(.,"{camera_name}")]]')

    def ERASE(self, box):
        return (By.XPATH, f'{box}/.//*[contains(@class,"deicon")]')

