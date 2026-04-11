from pages.playwright.base_page_playwright import BasePagePw


class HomePagePw(BasePagePw):
    def __init__(self, page):
        super().__init__(page)

    # --- URL's ---
    HOME_PAGE_URL = "https://demos.telerik.com/kendo-ui/eshop"
    REGISTRATION_PAGE_URL = "https://demos.telerik.com/kendo-ui/eshop/Account/Register"
    LOGIN_PAGE_URL = "https://demos.telerik.com/kendo-ui/eshop/Account/Login"
    CATEGORY_BIKES_URL = "https://demos.telerik.com/kendo-ui/eshop/Home/Bikes"

    # --- LOKATORY ---
    LOGOUT_BUTTON = "//a[contains(@class, 'k-menu-link') and text()='Logout']"
    MAIN_LOGIN_LINK = "//button[@type='submit' and contains(., 'Login')]"

    """Navigation methods"""

    def open_home_page_pw(self):
        print(f"[POM] Nawiguję do strony głównej: {self.HOME_PAGE_URL}")
        self.open(self.HOME_PAGE_URL)
        return self

    def open_login_page_pw(self):
        print(f"[POM] Nawiguję do strony logowania")
        self.open(self.LOGIN_PAGE_URL)
        return self

    def open_register_page_pw(self):
        print(f"[POM] Nawiguję do strony rejestracji")
        self.open(self.REGISTRATION_PAGE_URL)
        return self

    def click_logout_button_pw(self):
        print(f"[POM] Klikam przycisk wylogowania (JS)")
        self.js_click(self.LOGOUT_BUTTON)
        return self

    """Verification methods"""

    def is_logout_button_displayed_pw(self):
        print(f"[POM] Sprawdzam czy przycisk wylogowania jest widoczny...")
        is_visible = self.page.locator(self.LOGOUT_BUTTON).count() > 0
        if is_visible:
            print(f"[SUCCESS] Przycisk wylogowania znaleziony.")
        else:
            print(f"[WARNING] Przycisk wylogowania nie został znaleziony.")
        return is_visible