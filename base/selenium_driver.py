import time
from traceback import print_stack
from selenium.common.exceptions import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import utilities.custom_logger as cl
import logging
import os


class SeleniumDriver():
    log = cl.customLogger(logging.DEBUG)

    def __init__(self, driver):
        self.driver = driver

    def screenShot(self, resultMessage):
        """
        Takes screenshots of the current open web page
        """
        fileName = resultMessage + "_" + str(round(time.time() * 1000)) + ".png"
        screenshotsDirectory = "../screenshots/"
        relativeFileName = screenshotsDirectory + fileName
        currentDirectory = os.path.dirname(__file__)
        destinationFile = os.path.join(currentDirectory, relativeFileName)
        destinationDirectory = os.path.join(currentDirectory, screenshotsDirectory)

        try:
            if not os.path.exists(destinationDirectory):
                os.makedirs(destinationDirectory)
            self.driver.save_screenshot(destinationFile)
            self.log.info("Screenshots save to directory: " + destinationFile)
        except:
            self.log.error("### Exception Occured")
            print_stack()

    def getTitle(self):
        return self.driver.title

    def getByType(self, locatorType):
        locatorType = locatorType.lower()
        if locatorType == "id":
            return By.ID
        elif locatorType == "name":
            return By.NAME
        elif locatorType == "xpath":
            return By.XPATH
        elif locatorType == "css":
            return By.CSS_SELECTOR
        elif locatorType == "class":
            return By.CLASS_NAME
        elif locatorType == "link":
            return By.LINK_TEXT
        else:
            self.log.info("This Locator type is not supported")
        return False

    def getElement(self, locator, locatorType="id"):
        element = None
        try:
            locatorType = locatorType.lower()
            byType = self.getByType(locatorType)
            element = self.driver.find_element(byType, locator)
            self.log.info("Element Found with locator: " + locator + " and locatorType: " + locatorType)
        except:
            self.log.info("Element Not found with locator: " + locator + " and locatorType: " + locatorType)
        return element

    def getElementList(self, locator, locatorType="id"):
        element = None
        try:
            locatorType = locatorType.lower()
            byType = self.getByType(locatorType)
            elements = self.driver.find_elements(byType, locator)
            self.log.info("Element list Found with locator: " + locator + " and locatorType: " + locatorType)
        except:
            self.log.info("Element list Not found with locator: " + locator + " and locatorType: " + locatorType)
        return element

    def elementClick(self, locator="", locatorType="id", element=None):
        try:
            if locator:  # This means if locator is not empty
                element = self.getElement(locator, locatorType)
            element.click()
            self.log.info("Clicked on element with locator: " + locator + " locatorType: " + locatorType)
        except:
            self.log.info("Cannot click the element" + locator + " locatorType: " + locatorType)
            print_stack()

    def sendKeys(self, data, locator="", locatorType="id", element=None):
        try:
            if locator:  # This means if locator is not empty
                element = self.getElement(locator, locatorType)
            element.send_keys(data)
            self.log.info("Send data on element with locator: " + locator + " locatorType: " + locatorType)
        except:
            self.log.info("Cannot send data the element" + locator + " locatorType: " + locatorType)
            print_stack()

    def getText(self, locator="", locatorType="id", element=None, info=""):
        try:
            if locator:
                self.log.debug("In the locator condition")
                element = self.getElement(locator, locatorType)
            self.log.debug("Before finding text")
            text = element.text
            self.log.debug("After finding element, size is: " + str(len(text)))
            if len(text) == 0:
                text = element.get_attribute("innerText")
            if len(text) != 0:
                self.log.info("Getting text on element :: " + info)
                self.log.info("The text is :: '" + text + "'")
                text = text.strip()
        except:
            self.log.error("Failed to get text on element " + info)
            print_stack()
            text = None
        return text

    def isElementPresent(self, locator="", locatorType="id", element=None):
        try:
            if locator:
                element = self.getElement(locator, locatorType)
            if element is not None:
                print("Element Found")
                return True
            else:
                return False
        except:
            self.log.info("Element Not found")
            return False

    def isElementDisplayed(self, locator="", locatorType="id", element=None):

        isDisplayed = False
        try:
            if locator:
                element = self.getElement(locator, locatorType)
            if element is not None:
                isDisplayed = element.is_displayed()
                self.log.info("Element is displayed with locator: " + locator + " locator Type: " + locatorType)
            else:
                self.log.error("Element not displayed with locator: " + locator + " locator Type: " + locatorType)

            return isDisplayed
        except:
            self.log.error("Element not found")
            return False

    def elementPresentCheck(self, locator, byType):
        try:
            element_list = self.driver.find_elements(byType, locator)
            if len(element_list) > 0:
                self.log.info("Element Found")
                return True
            else:
                self.log.info("Element Not found")
                return False
        except:
            return False

    def waitForElement(self, locator, locatorType="id",
                       timeout=10, pollFrequency=0.5):
        element = None
        try:
            byType = self.getByType(locatorType)
            self.log.info("Waiting for Maximum:: " + str(timeout) +
                          ":: seconds for the element to be clickable")
            wait = WebDriverWait(self.driver, timeout=timeout, poll_frequency=1,
                                 ignored_exceptions=[NoSuchElementException,
                                                     ElementNotVisibleException,
                                                     ElementNotSelectableException])
            element = wait.until(EC.element_to_be_clickable(byType, "stopFilter_stops-0"))
            self.log.info("Element appeared on the page")

        except:
            self.log.info("ELement not appeared on the page")
            print_stack()
        return element

    def webScroll(self, direction="up"):
        if direction == "up":
            self.driver.execute_script("window.scrollBy(0, -1080);")
        if direction == "down":
            self.driver.execute_script("window.scrollBy(0, 1080);")

    def switchToFrame(self, id="", name="", index=None):
        """
        Switch to iFrame using element locator inside iframe
        :param id:
        :param name:
        :param index:
        :return:
        """
        try:
            if id:
                self.driver.switch_to.frame(id)
                self.log.info("Inside iFrame: " + id)
            elif name:
                self.driver.switch_to.frame(name)
                self.log.info("Inside iFrame: " + name)
            else:
                self.driver.switch_to.frame(index)
                self.log.info("Inside iFrame: " + name)
        except:
            self.log.error("Unable to find iFrame")

    def switchToDefaultContent(self):
        self.driver.switch_to.default_content()
        self.log.info("Switched to Parent window")

    def getElementAttributeValue(self, attribute, element=None, locator="", locatorType="id"):
        """
        Get value of the attribute of element
        :param attribute: attribute whose value to find
        :param element:
        :param locator:
        :param locatorType:
        :return:
        """
        if locator:
            element = self.getElement(locator=locator, locatorType=locatorType)
        value = element.get_attribute(attribute)
        return value

    def isEnabled(self, locator="", locatorType="id", info=""):
        """
                Check if element is enabled

                Parameters:
                    1. Required:
                        1. locator - Locator of the element to check
                    2. Optional:
                        1. locatorType - Type of the locator(id(default), xpath, css, className, linkText)
                        2. info - Information about the element, label/name of the element
                Returns:
                    boolean
                Exception:
                    None
                """
        element = self.getElement(locator, locatorType=locatorType)
        enabled = False
        try:
            attributeValue = self.getElementAttributeValue(element=element, attribute="disabled")
            if attributeValue is not None:
                enabled = element.is_enabled()
            else:
                value = self.getElementAttributeValue(element=element, attribute="class")
                self.log.info("Attribute value From Application Web UI --> :: " + value)
                enabled = not ("disabled" in value)
            if enabled:
                self.log.info("Element :: '" + info + "' is enabled")
            else:
                self.log.info("Element :: '" + info + "' is not enabled")
        except:
            self.log.error("Element :: '" + info + "' state could not be found")
        return enabled

    def pageNavigation(self, direction="back"):
        if direction == "back":
            self.driver.back()
        if direction == "forward":
            self.driver.forward()
