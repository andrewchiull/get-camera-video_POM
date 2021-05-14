from selenium.webdriver.common.by import By


class LoginPageLocators:

    # locators
    USERNAME_TEXT_FIELD = (By.XPATH, '//*[@name="textfield2"]')
    PASSWORD_TEXT_FIELD = (By.XPATH, '//*[@name="textfield"]')
    LOGIN_BUTTON = (By.XPATH, '//*[@class="btn-blue"]')

