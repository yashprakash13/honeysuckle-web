import os
import time

import pytest
from django.urls import reverse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


def take_screenshot(driver, name):
    time.sleep(1)
    os.makedirs(os.path.join("screenshots", os.path.dirname(name)), exist_ok=True)
    driver.save_screenshot(os.path.join("screenshots", name))


@pytest.mark.usefixtures("driver_init")
class SeleniumTest_all:
    def test_screenshot_about(self, live_server, use_debug_true_for_selenium_tests):
        self.driver.get(("%s%s" % (live_server.url, "/about/")))
        # take_screenshot(self.driver, "about_page" + self.browser + ".png")
        assert "His Brown Eyed Girl (HBEG)" in self.driver.page_source

    def test_login(self, live_server, new_admin_user):
        # test login and then profile page access
        self.driver.get(("%s%s" % (live_server.url, "/itisme/")))
        assert "Log in | Django site admin" in self.driver.title
        username_field = self.driver.find_element_by_name("username")
        password_field = self.driver.find_element_by_name("password")
        username_field.send_keys("test_admin_user")
        password_field.send_keys("test_password")
        password_field.send_keys(Keys.RETURN)
        self.driver.get(("%s%s" % (live_server.url, "/profiles/me/")))
        # time.sleep(10)
        assert "test_admin_user" in self.driver.page_source
