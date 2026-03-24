from selenium.webdriver.common.by import By
from pages.selenium.base_page_selenium import BasePage


class LoginPage(BasePage):
    TEST_USER_EMAIL = "jaxons.danniels@company.com"
    TEST_USER_PASS = "User1234"
"""
Login page locators
"""
LOGIN_FIELD = (By.XPATH, "//input[@data-role='textbox' and @id='Email']")
PASSWORD_FIELD = (By.XPATH, "//input[@data-role='textbox' and @type='password']")
LOGIN_BUTTON = (By.XPATH, "//button[@type='submit']")

"""
Methodes
"""


def click_email(self):
    self.driver.find_element_by_xpath(LOGIN_FIELD).click()


def click_password(self):
    self.driver.find_element_by_xpath(PASSWORD_FIELD).click()


def click_login_button(self):
    self.driver.find_element_by_xpath(LOGIN_BUTTON).click()

def login_as_correct_user(self, email, password):
    self.driver.find_element_by_xpath(LOGIN_FIELD).click()
    self.driver.find_element_by_xpath(LOGIN_FIELD).clear()
    self.driver.find_element_by_xpath(LOGIN_FIELD).send_keys()
