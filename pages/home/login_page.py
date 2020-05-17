import time

import utilities.custom_logger as cl
import logging
from base.basepage import BasePage
from pages.home.navigation_header_page import NavigationPage

class LoginPage(BasePage):
    log = cl.customLogger(logging.DEBUG)

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        self.nav = NavigationPage(self.driver)

    # Locators
    __login_link = "Login"
    _email_field = "user_email"
    _password_field = "user_password"
    _login_button = "commit"
    _logout_Button = "//div[@id='navbar']//a[@href='/sign_out']"

    def clickLoginLink(self):
        self.elementClick(self.__login_link, locatorType="link")

    def enterEmail(self, email):
        self.sendKeys(email, self._email_field)

    def enterPassword(self, password):
        self.sendKeys(password, self._password_field)

    def clickLoginButton(self):
        self.elementClick(self._login_button, locatorType="name")

    def clickLogoutButton(self):
        self.elementClick(self._logout_Button, locatorType="xpath")

    def login(self, email="", password=""):
        self.clickLoginLink()
        self.enterEmail(email)
        self.enterPassword(password)
        time.sleep(5)
        self.clickLoginButton()

    def verifyLoginSuccessful(self):
        result = self.isElementPresent("search-courses", "id")
        return result

    def verifyLoginFailed(self):
        result = self.isElementPresent("//div[contains(text(), 'Invalid email or password')]", locatorType="xpath")
        return result

    def verifyLoginTiltle(self):
        return self.verifyPageTitle("Let's Kode It")

    def logout(self):
        self.nav.navigateToUserIcon()
        self.clickLogoutButton()

