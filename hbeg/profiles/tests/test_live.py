import os
import time

import pytest
from django.urls import reverse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


def take_screenshot(driver, name):
    """a helper func to take any screenshot"""
    time.sleep(1)
    os.makedirs(os.path.join("screenshots", os.path.dirname(name)), exist_ok=True)
    driver.save_screenshot(os.path.join("screenshots", name))


@pytest.mark.usefixtures("driver_init")
class SeleniumTest_all:
    def test_screenshot_about(self, live_server, use_debug_true_for_selenium_tests):
        """take screenshot of about page"""
        self.driver.get(("%s%s" % (live_server.url, "/about/")))
        # take_screenshot(self.driver, "about_page" + self.browser + ".png")
        assert "His Brown Eyed Girl (HBEG)" in self.driver.page_source

    def test_login(self, live_server, new_admin_user):
        """test new user create/ login + access to profile page"""
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

    # def test_story_search_add_to_folder_and_rate(self, live_server, new_admin_user):
    #     # make a user and login with that user
    #     self.driver.get(("%s%s" % (live_server.url, "/itisme/")))
    #     assert "Log in | Django site admin" in self.driver.title
    #     username_field = self.driver.find_element_by_name("username")
    #     password_field = self.driver.find_element_by_name("password")
    #     username_field.send_keys("test_admin_user")
    #     password_field.send_keys("test_password")
    #     password_field.send_keys(Keys.RETURN)

    #     # make a new folder
    #     self.driver.get(("%s%s" % (live_server.url, "/profiles/me/")))
    #     self.driver.find_element_by_id("new-folder-button").click()
    #     time.sleep(1)
    #     name_field = self.driver.find_element_by_name("folder_name")
    #     name_field.send_keys("test_folder_name")
    #     desc_field = self.driver.find_element_by_name("folder_desc")
    #     desc_field.send_keys("test_folder_desc")
    #     self.driver.find_element_by_id("folder-add-save-btn").click()
    #     assert "test_folder_name" in self.driver.page_source

    #     # insert story into that folder
    #     self.driver.get(("%s%s" % (live_server.url, "")))
    #     search_field = self.driver.find_element_by_name("query")
    #     search_field.send_keys("a:tyrannicpuppy elfish")
    #     search_field.send_keys(Keys.RETURN)
    #     time.sleep(10)
    #     self.driver.find_element_by_id("title-of-fic").click()
    #     assert "Read this story? Rate it now!" in self.driver.page_source
    #     self.driver.find_element_by_id("story-add-to-folder-btn").click()
    #     checkboxes = self.driver.find_elements_by_name("folder_checkboxes")
    #     for checkbox in checkboxes:
    #         checkbox.click()
    #     self.driver.find_element_by_id("add-story-to-folder-btn").click()

    #     # go to profile -> check folder for that story is there
    #     self.driver.get(("%s%s" % (live_server.url, "/profiles/me/")))
    #     time.sleep(3)
    #     assert "tyrannicpuppy" in self.driver.page_source
