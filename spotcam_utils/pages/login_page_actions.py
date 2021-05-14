import time
import logging

from spotcam_utils.base_page import BasePage
from spotcam_utils.pages.login_page_locators import LoginPageLocators


class LoginPage(BasePage):

    login_locators = LoginPageLocators

    def get_login_page(self):
        url = "https://www.myspotcam.com/tc/welcome/login"
        self.get_page(url)

    def input_username(self, username):
        self.find_element(self.login_locators.USERNAME_TEXT_FIELD).send_keys(username)

    def input_password(self, password):
        self.find_element(self.login_locators.PASSWORD_TEXT_FIELD).send_keys(password)

    def click_login_button(self):
        self.find_element(self.login_locators.LOGIN_BUTTON).click()
        self.wait_page_until_loading()
