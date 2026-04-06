from pages.playwright.base_page_playwright import BasePage

"""
Home Page Object for each page (Playwright)
"""

class HomePage(BasePage):
    HOME_PAGE_URL = "https://demos.telerik.com/kendo-ui/eshop"
    REGISTRATION_PAGE_URL = "https://demos.telerik.com/kendo-ui/eshop/Account/Register"
    LOGIN_PAGE_URL = "https://demos.telerik.com/kendo-ui/eshop/Account/Login"

    def open_home_page(self):
        self.open(self.HOME_PAGE_URL)

    def open_register_page(self):
        self.open(self.REGISTRATION_PAGE_URL)

    def open_login_page(self):
        self.open(self.LOGIN_PAGE_URL)
