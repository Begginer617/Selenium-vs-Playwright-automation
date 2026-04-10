from pages.playwright.base_page_playwright import BasePagePw


class LoginPagePw(BasePagePw):
    def __init__(self, page):
        super().__init__(page)  # To jest KLUCZOWE

    ADMIN_TEST_USER_EMAIL = "jaxons.danniels@company.com"
    ADMIN_TEST_USER_PASS = "User1234"
    EMAIL_FIELD = "#Email"
    PASSWORD_FIELD = "#Password"

    def login_as_admin_pw(self):
        self.type(self.EMAIL_FIELD, self.ADMIN_TEST_USER_EMAIL)
        self.type(self.PASSWORD_FIELD, self.ADMIN_TEST_USER_PASS)
        self.page.locator(self.PASSWORD_FIELD).press("Enter")