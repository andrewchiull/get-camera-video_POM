# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re

class AppDynamicsJob(unittest.TestCase):
    def setUp(self):
        # AppDynamics will automatically override this web driver
        # as documented in https://docs.appdynamics.com/display/PRO44/Write+Your+First+Script
        self.driver = webdriver.Chrome('spotcam_utils/browser_driver/chromedriver')
        self.driver.implicitly_wait(30)
        self.base_url = "https://www.google.com/"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_app_dynamics_job(self):
        driver = self.driver
        driver.get("https://www.myspotcam.com/tc/welcome/login")
        driver.find_element_by_id("email").click()
        driver.find_element_by_id("email").clear()
        driver.find_element_by_id("email").send_keys("a50202jim@gmail.com")
        driver.find_element_by_id("password").click()
        driver.find_element_by_id("password").clear()
        driver.find_element_by_id("password").send_keys("303303303")
        driver.find_element_by_xpath(u"//a[contains(text(),'登入')]").click()
        driver.find_element_by_link_text("BIME-YunLin").click()
        driver.find_element_by_css_selector("a.setDate > span.text.textM").click()
        driver.find_element_by_css_selector("li.Ymd-19 > span.text.textM.textCalendar").click()
        driver.find_element_by_css_selector(u"i.icon.iconEvent > #圖層_1").click()
        driver.find_element_by_css_selector("span.filterText").click()
        driver.find_element_by_css_selector("a.senseFilter.motionBtn > span.text").click()
        driver.find_element_by_css_selector("div.event.motion_filter > div.eventInfo").click()
        driver.find_element_by_css_selector(u"i.icon.iconFilm > #分離模式").click()
        driver.find_element_by_id("export_select_month").click()
        Select(driver.find_element_by_id("export_select_month")).select_by_visible_text("05")
        driver.find_element_by_id("export_select_date").click()
        Select(driver.find_element_by_id("export_select_date")).select_by_visible_text("14")
        driver.find_element_by_id("export_select_hour").click()
        Select(driver.find_element_by_id("export_select_hour")).select_by_visible_text("12")
        driver.find_element_by_id("export_select_minute").click()
        Select(driver.find_element_by_id("export_select_minute")).select_by_visible_text("29")
        driver.find_element_by_id("export_length").click()
        driver.find_element_by_xpath("//div[@id='mkfilm']/div/div/div[2]/div/div[4]/a[2]").click()
        driver.find_element_by_xpath("//div[@id='alertCustomised']/div/div/a").click()
        driver.find_element_by_link_text(u"我的影片").click()
        driver.find_element_by_xpath("//div[@id='nowcenttbox']/div/div[3]/div/div[56]/p").click()
        driver.find_element_by_xpath("//div[@id='nowcenttbox']/div/div[3]/div/div[56]/p").click()
        driver.find_element_by_xpath("(//a[contains(text(),'BIME-YunLin')])[56]").click()
        driver.find_element_by_css_selector("button.vjs-big-play-button").click()
        driver.find_element_by_css_selector("a[title=\"Download\"] > img").click()
        driver.find_element_by_css_selector("a.fancybox-item.fancybox-close").click()
        self.accept_next_alert = True
        driver.find_element_by_xpath("//div[@id='nowcenttbox']/div/div[3]/div/div[56]/a[2]").click()
        self.assertEqual(u"你確定要刪除這個影像嗎？", self.close_alert_and_get_its_text())
    
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e: return False
        return True
    
    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException as e: return False
        return True
    
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True
    
    def tearDown(self):
        # To know more about the difference between verify and assert,
        # visit https://www.seleniumhq.org/docs/06_test_design_considerations.jsp#validating-results
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
