from selenium.webdriver.common.by import By

from BaseShit.BaseClass import BaseClass
from pageObjects.VisitorRegistrationPage import VisitorRegistrationPage


class LoginPage(BaseClass):

    def __init__(self, driver):
        self.driver = driver

    email_locator = (By.ID, "username")
    password_locator = (By.ID, "password")
    login_locator = (By.XPATH, "//button[.='Login']")
    register_visitor_locator = (By.XPATH, "//a[contains(text(), 'visitor')]")

    def get_visitor_registration(self):
        self.driver.find_element(*LoginPage.register_visitor_locator).click()
        visitor_registration_page = VisitorRegistrationPage(self.driver)
        return visitor_registration_page

    def get_email_field(self):
        return self.driver.find_element(*LoginPage.email_locator)

    def get_password_field(self):
        return self.driver.find_element(*LoginPage.password_locator)

    def get_login_button(self):
        return self.driver.find_element(*LoginPage.login_locator).click()
