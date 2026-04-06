from selenium.webdriver.common.by import By
from pages.selenium.base_page_selenium import BasePage

class HomePage(BasePage):
    # --- URL's ---
    HOME_PAGE_URL = "https://demos.telerik.com/kendo-ui/eshop"
    REGISTRATION_PAGE_URL = "https://demos.telerik.com/kendo-ui/eshop/Account/Register"
    LOGIN_PAGE_URL = "https://demos.telerik.com/kendo-ui/eshop/Account/Login"
    CATEGORY_BIKES_URL = "https://demos.telerik.com/kendo-ui/eshop/Home/Bikes"

    # --- LOKATORY ---
    LOGOUT_BUTTON = (By.XPATH, "//a[contains(text(), 'Logout')]")
    MAIN_LOGIN_LINK = (By.XPATH, "//button[@type='submit' and contains(., 'Login')]")
    REGISTRATION_LOGIN_LINK=(By.XPATH, "//p[contains(text(), 'Already have an account?')]/following-sibling::a")
    """
    Navigation methods
    """
    def open_home_page(self):
        self.open(self.HOME_PAGE_URL)

    def open_register_page(self):
        self.open(self.REGISTRATION_PAGE_URL)

    def open_login_page(self):
        self.open(self.LOGIN_PAGE_URL)

    """
    Verification methods
    """
    def is_logout_button_displayed(self):
        # Wykorzystujemy self.wait_for_visible z BasePage
        # Jeśli przycisk się nie pojawi, wait wyrzuci TimeoutException (i screenshot w Allure!)
        try:
            return self.wait_for_visible(self.LOGOUT_BUTTON).is_displayed()
        except:
            return False