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
    LOGOUT_BUTTON = "//a[contains(@class, 'k-menu-link') and text()='Logout']"

    def login_as_admin_pw(self):
        print(f"[POM] Filling email field: {self.ADMIN_TEST_USER_EMAIL}")
        self.page.fill(self.LOGIN_FIELD, self.ADMIN_TEST_USER_EMAIL)

        print("[POM] Filling password field")
        self.page.fill(self.PASSWORD_FIELD, self.ADMIN_TEST_USER_PASS)

        print("[POM] Clicking login button...")
        self.page.click(self.LOGIN_BUTTON)

        print("[POM] Waiting for post-login state...")
        self.wait_for_url("/eshop")
        self.wait_for_visible(self.LOGOUT_BUTTON)
        print("[SUCCESS] Login completed successfully.")

        return self

    def is_logged_in_pw(self):
        return self.page.locator(self.LOGOUT_BUTTON).first.is_visible()

    def expect_logged_in_pw(self):
        expect(self.page.locator(self.LOGOUT_BUTTON).first).to_be_visible(timeout=self.timeout_ms)