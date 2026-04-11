from playwright.sync_api import Page
from pages.playwright.base_page_playwright import BasePagePw

class LoginPagePw(BasePagePw):
    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page

    ADMIN_TEST_USER_EMAIL = "jaxons.danniels@company.com"
    ADMIN_TEST_USER_PASS = "User1234"

    # Lokatory (używamy stringów CSS/XPath)
    LOGIN_FIELD = "#Email"
    PASSWORD_FIELD = "#Password"
    LOGIN_BUTTON = ".k-form-submit"

    def login_as_admin_pw(self):
        self.page.fill(self.LOGIN_FIELD, self.ADMIN_TEST_USER_EMAIL)
        self.page.fill(self.PASSWORD_FIELD, self.ADMIN_TEST_USER_PASS)
        self.page.click(self.LOGIN_BUTTON)
        self.page.wait_for_url("**/eshop") # Czekaj na przekierowanie
        return self