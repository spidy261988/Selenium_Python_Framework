import time

import pytest
from selenium import webdriver
from pages.courses.register_courses_page import RegisterCoursesPage
import unittest
from utilities.teststatus import TestStatus
from ddt import ddt, data, unpack
from utilities.read_data import getCSVData
from pages.home.navigation_header_page import NavigationPage

@pytest.mark.usefixtures("oneTimeSetUp", "setUp")
@ddt
class RegisterCoursesCSVDataTests(unittest.TestCase):

    @pytest.fixture(autouse=True)
    def objectSetup(self, oneTimeSetUp):
        self.courses = RegisterCoursesPage(self.driver)
        self.ts = TestStatus(self.driver)

    def setUp(self) -> None:
        self.driver.get("https://learn.letskodeit.com/courses")

    @pytest.mark.run(order=1)
    @data(*getCSVData("C:\\Users\\ranjit.show\\PycharmProjects\\workspace_python\\letskodeit\\csvData.csv"))
    @unpack
    def test_invalidEnrollment(self, courseName, ccNum, ccExp, ccCVV, zip):
        self.courses.enterCourseName(courseName)
        self.courses.clickSearchCourseButton()
        self.courses.selectCourseToEnroll(courseName)
        self.courses.enrollCourse(num=ccNum, exp=ccExp, cvv=ccCVV, zip=zip)
        result = self.courses.verifyEnrollFailed()
        self.ts.markFinal("test_invalidEnrollment", result, "Enrollment Verification")
