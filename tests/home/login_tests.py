import time

import pytest
from selenium import webdriver
from pages.home.login_page import LoginPage
import unittest
from utilities.teststatus import TestStatus


@pytest.mark.usefixtures("oneTimeSetUp", "setUp")
class LoginTests(unittest.TestCase):

    @pytest.fixture(autouse=True)
    def classSetup(self, oneTimeSetUp):
        self.lp = LoginPage(self.driver)
        self.ts = TestStatus(self.driver)

    @pytest.mark.run(order=2)
    def test_valid_login(self):
        self.lp.login("test@email.com", "abcabc")
        result1 = self.lp.verifyLoginTiltle()
        self.ts.mark(result1, "Title verification")
        result2 = self.lp.verifyLoginSuccessful()
        self.ts.markFinal("test_valid_login", result2, "Login verification")

    @pytest.mark.run(order=1)
    def test_invalid_login(self):
        self.lp.logout()
        self.lp.login(password="abcabcabc")
        result = self.lp.verifyLoginFailed()
        assert result == True
