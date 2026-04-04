from pages.playwright.base_page_playwright import BasePage


class LoginPage(BasePage):
    ADMIN_TEST_USER_EMAIL = "jaxons.danniels@company.com"
    ADMIN_TEST_USER_PASS = "User1234"

    EMAIL_FIELD = "#Email"
    PASSWORD_FIELD = "#Password"

    def open_login_page(self):
        self.open("https://demos.telerik.com/kendo-ui/eshop/Account/Login")

    def login_as_admin(self):
        self.type(self.EMAIL_FIELD, self.ADMIN_TEST_USER_EMAIL)
        self.type(self.PASSWORD_FIELD, self.ADMIN_TEST_USER_PASS)
        self.page.locator(self.PASSWORD_FIELD).press("Enter")
