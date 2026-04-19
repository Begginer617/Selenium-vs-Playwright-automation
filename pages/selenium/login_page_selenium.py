from selenium.webdriver.common.by import By
from pages.selenium.base_page_selenium import BasePage
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException


class LoginPage(BasePage):

    """Credentials"""
    ADMIN_TEST_USER_EMAIL = "jaxons.danniels@company.com"
    ADMIN_TEST_USER_PASS = "User1234"

    """Login page locators."""
    LOGIN_FIELD = (By.ID, "Email")
    PASSWORD_FIELD = (By.ID, "Password")
    LOGIN_BUTTON = (By.CSS_SELECTOR, ".k-form-submit")
    LOGOUT_BUTTON = (By.XPATH, "//a[contains(@class, 'k-menu-link') and normalize-space()='Logout']")
    """Methods using BasePage actions and waits."""

    def login_as_admin(self):
        self.type(self.LOGIN_FIELD, self.ADMIN_TEST_USER_EMAIL)
        self.type(self.PASSWORD_FIELD, self.ADMIN_TEST_USER_PASS)

        # Submit with Enter to keep behavior close to manual user flow.
        password_element = self.wait_for_visible(self.PASSWORD_FIELD)
        password_element.send_keys(Keys.ENTER)

        # Explicit post-login waits to avoid returning too early.
        self.wait_for_url("/eshop", timeout=12)
        self.wait_for_visible(self.LOGOUT_BUTTON, timeout=12)
        return self

    def is_logged_in(self):
        try:
            return self.wait_for_visible(self.LOGOUT_BUTTON, timeout=6).is_displayed()
        except TimeoutException:
            return False



