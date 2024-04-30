import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from BaseShit.BaseClass import BaseClass
from TestData.LoginPageData import HomePageData
from pageObjects.LoginPage import LoginPage
from pageObjects.VisitorRegistrationPage import VisitorRegistrationPage
import pytest


@pytest.mark.usefixtures("setup")
class TestOne(BaseClass):

    def test_login(self, get_data):
        log = self.get_logger()
        login_page = LoginPage(self.driver)
        email_field = login_page.get_email_field()
        email_field.send_keys(get_data["email"])
        log.info("Email is successfully filed")
        password_field = login_page.get_password_field()
        password_field.send_keys(get_data["password"])
        log.info("Password is successfully filed")
        login_page.get_login_button()
        error_message_element = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".form-error"))
        )

        print("Test text")
        assert "Email and password combination not valid" in error_message_element.text

        # visitor_registration_page = login_page.get_visitor_registration()
        # visitor_registration_page.get_visitor_email().send_keys(get_data[1])
        time.sleep(2)
        self.driver.refresh()

    @pytest.fixture(params=HomePageData.get_test_data("TestCase2"))
    def get_data(self, request):
        return request.param
