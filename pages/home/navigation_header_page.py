import time

import utilities.custom_logger as cl
import logging
from base.basepage import BasePage


class NavigationPage(BasePage):
    log = cl.customLogger(logging.DEBUG)

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    # Locators
    __my_courses = "My Courses"
    _all_courses = "All Courses"
    _practice = "Practice"
    _user_icon = "//img[@class = 'gravatar']"

    def navigateToMyCourses(self):
        self.elementClick(locator=self.__my_courses, locatorType="link")

    def navigateToAllCourses(self):
        self.elementClick(locator=self._all_courses, locatorType="link")

    def navigateToPractice(self):
        self.elementClick(locator=self._practice, locatorType="link")

    def navigateToUserIcon(self):
        self.elementClick(locator=self._user_icon, locatorType="xpath")