import time

import pyautogui
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

driver = None


def pytest_addoption(parser):
    parser.addoption(
        "--browser_name", action="store", default="chrome"
    )


@pytest.fixture(scope="class")
def setup(request):
    global driver
    # If you need to do any setup before tests, you can do it here
    browser_name = request.config.getoption("browser_name")
    if browser_name == "chrome":
        driver = webdriver.Chrome()
    elif browser_name == "firefox":
        driver = webdriver.Firefox()
    elif browser_name == "edge":
        driver = webdriver.Edge()
    driver.implicitly_wait(5)
    wait = WebDriverWait(driver, 30)
    driver.get("https://www.kinky.dev.sceon.am/inloggen")
    driver.maximize_window()

    # # Kinky staging login via alert
    # pyautogui.write("kinky")
    # pyautogui.press("tab")  # Move to the password field
    # pyautogui.write("Zz123456")
    # pyautogui.press("enter")

    # Changing language
    driver.find_element(By.CSS_SELECTOR, "div#termsPopup img.flag").click()

    # Get flags as list and select english
    flags = driver.find_elements(By.XPATH, "//div[@class='dropdown-item popup-switcher']")
    for flag in flags:
        if flag.get_attribute("data-lang") == 'en':
            flag.click()
            break

    # Check if the selected language is en
    assert driver.find_element(By.XPATH, "//a[@data-toggle='dropdown']/img").get_attribute("alt") == "en"

    # Cookies toggles on
    toggles = driver.find_elements(By.XPATH, "//span[@class='slider round']")
    for toggle in toggles:
        toggle.click()

    # Wait until button is enabled and click on it
    wait.until_not(expected_conditions.presence_of_element_located((By.XPATH, "//button[@disabled]")))
    driver.find_element(By.CSS_SELECTOR, ".__submit").click()

    # If you need to do any setup before tests, you can do it here

    request.cls.driver = driver
    yield

    # If you need to do any steps after tests, you can do it here
    driver.close()


@pytest.mark.hookwrapper
def pytest_runtest_makereport(item):
    """
        Extends the PyTest Plugin to take and embed screenshot in html report, whenever test fails.
        :param item:
        """
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, 'extra', [])

    if report.when == 'call' or report.when == "setup":
        xfail = hasattr(report, 'wasxfail')
        if (report.skipped and xfail) or (report.failed and not xfail):
            file_name = report.nodeid.replace("::", "_") + ".png"
            screenshot_path = r"C:\Users\EF\Desktop\Python selenium testing\Kinky\reports\\"

            _capture_screenshot(file_name, screenshot_path)
            if file_name:
                html = '<div><img src="%s" alt="screenshot" style="width:304px;height:228px;" ' \
                       'onclick="window.open(this.src)" align="right"/></div>' % file_name
                extra.append(pytest_html.extras.html(html))
        report.extra = extra


def _capture_screenshot(name, screenshot_path):
    driver.get_screenshot_as_file(screenshot_path + name)
