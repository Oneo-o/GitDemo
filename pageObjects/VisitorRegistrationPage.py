from selenium.webdriver.common.by import By

from BaseShit.BaseClass import BaseClass


class VisitorRegistrationPage(BaseClass):
    def __init__(self, driver):
        self.driver = driver

    visitorEmail_locator = (By.ID, "email")

    def get_visitor_email(self):
        return self.driver.find_element(*VisitorRegistrationPage.visitorEmail_locator)
