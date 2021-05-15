from selenium.webdriver.common.by import By


class LoginPageLocators:

    # locators
    USERNAME_TEXT_FIELD = (By.XPATH, '//*[@id="email"]')
    PASSWORD_TEXT_FIELD = (By.XPATH, '//*[@id="password"]')
    LOGIN_BUTTON = (By.XPATH, u"//a[contains(text(),'登入')]")

