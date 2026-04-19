from playwright.sync_api import Page, expect
from pages.playwright.base_page_playwright import BasePagePw


class LoginPagePw(BasePagePw):
    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page

    ADMIN_TEST_USER_EMAIL = "jaxons.danniels@company.com"
    ADMIN_TEST_USER_PASS = "User1234"

    # Locators
    LOGIN_FIELD = "#Email"
    PASSWORD_FIELD = "#Password"
    LOGIN_BUTTON = ".k-form-submit"
    AUTHENTICATED_FAVORITES_LINK = "//a[contains(@href, '/Account/Favorites')]"

    def login_as_admin_pw(self):
        self.log_step(f"Filling email field for user: {self.ADMIN_TEST_USER_EMAIL}")
        self.page.fill(self.LOGIN_FIELD, self.ADMIN_TEST_USER_EMAIL)

        self.log_step("Filling password field")
        self.page.fill(self.PASSWORD_FIELD, self.ADMIN_TEST_USER_PASS)

        self.log_step("Clicking login button")
        self.page.click(self.LOGIN_BUTTON)

        self.log_step("Waiting for post-login authenticated state")
        self.wait_for_url("/eshop")
        self.wait_for_visible(self.AUTHENTICATED_FAVORITES_LINK)
        self.log_done("Login completed successfully")

        return self

    def is_logged_in_pw(self):
        return self.page.locator(self.AUTHENTICATED_FAVORITES_LINK).first.is_visible()

    def expect_logged_in_pw(self):
        expect(self.page.locator(self.AUTHENTICATED_FAVORITES_LINK).first).to_be_visible(timeout=self.timeout_ms)