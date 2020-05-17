import time

import utilities.custom_logger as cl
import logging
from base.basepage import BasePage



class RegisterCoursesPage(BasePage):
    log = cl.customLogger(logging.DEBUG)

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    ################
    ### Locators ###
    ################
    _search_box = "search-courses"
    _search_course_button = "search-course-button"
    _course = "//div[contains(@class, 'course-listing-title') and contains(text(), '{0}')]"
    _all_courses = "//a[contains(text(), 'All Courses')]"
    _enroll_button = "enroll-button-top"
    _cc_num = "//input[@aria-label = 'Credit or debit card number']"
    _cc_exp = "//input[@aria-label = 'Credit or debit card expiration date']"
    _cc_cvv = "//input[@aria-label = 'Credit or debit card CVC/CVV']"
    _zip = "postal"
    _agree_terms = "agreed_to_terms_checkbox"
    _submit_enroll = "confirm-purchase"

    ############################
    ### Element Interactions ###
    ############################

    def enterCourseName(self, name):
        self.sendKeys(name, locator=self._search_box)

    def clickSearchCourseButton(self):
        self.elementClick(self._search_course_button, locatorType="id")

    def selectCourseToEnroll(self, fullCourseName):
        self.elementClick(locator=self._course.format(fullCourseName), locatorType="xpath")

    def clickAllCourses(self):
        self.elementClick(locator=self._all_courses, locatorType="xpath")

    def clickOnEnrollButton(self):
        self.elementClick(locator=self._enroll_button)

    def enterCardNum(self, num):
        self.switchToFrame(name="__privateStripeFrame5")
        self.sendKeys(num, locator=self._cc_num, locatorType="xpath")
        self.switchToDefaultContent()

    def enterCardExp(self, exp):
        self.switchToFrame(name="__privateStripeFrame6")
        self.sendKeys(exp, self._cc_exp, locatorType="xpath")
        self.switchToDefaultContent()

    def enterCardCVV(self, cvv):
        self.switchToFrame(name="__privateStripeFrame7")
        self.sendKeys(cvv, locator=self._cc_cvv, locatorType="xpath")
        self.switchToDefaultContent()

    def enterZip(self, zip):
        self.switchToFrame(name="__privateStripeFrame8")
        self.sendKeys(zip, locator=self._zip, locatorType="name")
        self.switchToDefaultContent()

    def clickAgreeToTermsCheckBox(self):
        self.elementClick(locator=self._agree_terms)

    def clickEnrollSubmitButton(self):
        self.elementClick(locator=self._submit_enroll, locatorType="id")

    def enterCreditCardInformation(self, num, exp, cvv, zip):
        self.enterCardNum(num)
        self.enterCardExp(exp)
        self.enterCardCVV(cvv)
        self.enterZip(zip)

    def enrollCourse(self, num="", exp="",cvv="", zip=""):
        self.clickOnEnrollButton()
        self.webScroll(direction="down")
        self.enterCreditCardInformation(num, exp, cvv, zip)
        self.clickAgreeToTermsCheckBox()

    def verifyEnrollFailed(self):
        result = self.isEnabled(locator=self._submit_enroll, locatorType="id", info="Enroll Button")

        return not result

