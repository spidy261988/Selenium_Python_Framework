import time

import pytest
from selenium import webdriver
from pages.courses.register_courses_page import RegisterCoursesPage
import unittest
from utilities.teststatus import TestStatus
from ddt import ddt, data, unpack

@pytest.mark.usefixtures("oneTimeSetUp", "setUp")
@ddt
class RegisterMultipleCoursesTests(unittest.TestCase):

    @pytest.fixture(autouse=True)
    def classSetup(self, oneTimeSetUp):
        self.courses = RegisterCoursesPage(self.driver)
        self.ts = TestStatus(self.driver)

    @pytest.mark.run(order=1)
    @data(("JavaScript for beginners", "1234 5678 9012 3456", "1220", "100", "12345"), ("Selenium WebDriver With Java", "1234 5678 9012 3456", "9875", "300", "12345"))
    @unpack
    def test_invalidEnrollment(self, courseName, ccNum, ccExp, ccCVV, zip):
        self.courses.enterCourseName(courseName)
        self.courses.clickSearchCourseButton()
        self.courses.selectCourseToEnroll(courseName)
        self.courses.enrollCourse(num=ccNum, exp=ccExp, cvv=ccCVV, zip=zip)
        result = self.courses.verifyEnrollFailed()
        self.ts.markFinal("test_invalidEnrollment", result, "Enrollment Verification")
        self.driver.get("https://learn.letskodeit.com/courses")
