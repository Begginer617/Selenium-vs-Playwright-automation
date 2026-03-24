from selenium.webdriver.common.by import By
from pages.selenium.base_page_selenium import BasePage


class HomePage(BasePage):
    # using home page for navigation between sites
    # --- URL's ---
    HOME_PAGE_URL = "https://demos.telerik.com/kendo-ui/eshop/"
    REGISTRATION_PAGE_URL = "https://demos.telerik.com/kendo-ui/eshop/Account/Register"
    LOGIN_PAGE_URL = "https://demos.telerik.com/kendo-ui/eshop/Account/Login"

    # --- LOKATORY ELEMENTÓW PO ZALOGOWANIU ---
    LOGOUT_BUTTON = (By.XPATH, "//a[contains(text(), 'Logout')]")
    LOGIN_LINK = (By.XPATH, "//a[contains(@href, '/Account/Login')]")

    """
    Navigation methods
    """

    def open_home_page(self):
        self.open(self.HOME_PAGE_URL)

    def open_register_page(self):
        self.open(self.REGISTRATION_PAGE_URL)

    def open_login_page(self):
        self.open(self.LOGIN_PAGE_URL)
