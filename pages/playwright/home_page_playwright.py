from pages.playwright.base_page_playwright import BasePagePw

class HomePagePw(BasePagePw): # Dodajemy dziedziczenie
    def __init__(self, page):
        super().__init__(page) # Przekazujemy 'page' do BasePagePw


    # --- URL's ---

    HOME_PAGE_URL = "https://demos.telerik.com/kendo-ui/eshop"
    REGISTRATION_PAGE_URL = "https://demos.telerik.com/kendo-ui/eshop/Account/Register"
    LOGIN_PAGE_URL = "https://demos.telerik.com/kendo-ui/eshop/Account/Login"
    CATEGORY_BIKES_URL = "https://demos.telerik.com/kendo-ui/eshop/Home/Bikes"

    # --- LOKATORY ---
    LOGOUT_BUTTON = "//a[contains(@class, 'k-menu-link') and text()='Logout']"
    MAIN_LOGIN_LINK = "//button[@type='submit' and contains(., 'Login')]"
    REGISTRATION_LOGIN_LINK = "//p[contains(text(), 'Already have an account?')]/following-sibling::a"

    """Navigation methods"""

    def open_home_page_pw(self):
        self.open(self.HOME_PAGE_URL)

    def open_login_page_pw(self):
        self.open(self.LOGIN_PAGE_URL)

    def open_register_page_pw(self):
        self.open(self.REGISTRATION_PAGE_URL)

    def click_logout_button(self):
        # Zamiast self.click(self.LOGOUT_BUTTON) używamy JS
        self.js_click(self.LOGOUT_BUTTON)

    """
    Verification methods
    """


    def is_logout_button_displayed(self):
    # Jeśli znaleziono przynajmniej 1 taki element w kodzie
        return self.page.locator(self.LOGOUT_BUTTON).count() > 0
