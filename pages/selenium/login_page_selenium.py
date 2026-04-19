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
    LOGIN_PAGE_URL_FRAGMENT = "Account/Login"
    LOGIN_ERROR_EMAIL = (By.XPATH, "//a[@data-field='Email' and contains(text(), 'not valid email')]")
    AUTHENTICATED_FAVORITES_LINK = (By.XPATH, "//a[contains(@href, '/Account/Favorites')]")
    """Methods using BasePage actions and waits."""

    def login_as_admin(self):
        for attempt in range(2):
            self.type(self.LOGIN_FIELD, self.ADMIN_TEST_USER_EMAIL)
            self.type(self.PASSWORD_FIELD, self.ADMIN_TEST_USER_PASS)

            if attempt == 0:
                # Primary path: click submit button.
                self.safe_click(self.LOGIN_BUTTON, retries=2)
            else:
                # Fallback path: submit with Enter for environments where click is flaky.
                self.wait_for_visible(self.PASSWORD_FIELD).send_keys(Keys.ENTER)

            try:
                self._wait(
                    lambda d: self.LOGIN_PAGE_URL_FRAGMENT not in d.current_url,
                    timeout=10,
                )
                self._wait(
                    lambda d: "Home Page" in d.title
                    or len(d.find_elements(*self.AUTHENTICATED_FAVORITES_LINK)) > 0,
                    timeout=10,
                )
                return self
            except TimeoutException:
                if attempt == 0:
                    # Retry once with Enter submit if click path did not complete authentication.
                    self.open("https://demos.telerik.com/kendo-ui/eshop/Account/Login")
                    continue
                raise

        return self

    def is_logged_in(self):
        try:
            self._wait(
                lambda d: self.LOGIN_PAGE_URL_FRAGMENT not in d.current_url
                and ("Home Page" in d.title or len(d.find_elements(*self.AUTHENTICATED_FAVORITES_LINK)) > 0),
                timeout=10,
            )
            return True
        except TimeoutException:
            return False



