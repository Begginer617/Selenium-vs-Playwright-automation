from pages.selenium.base_page_selenium import BasePage

class HomePage(BasePage):
    # Zmienna klasowa z adresem
    HOME_PAGE_URL = "https://demos.telerik.com/kendo-ui/eshop/"
    REGISTRATION_PAGE_URL = "https://demos.telerik.com/kendo-ui/eshop/Account/Register"

    def open_home_page(self):
        # Używamy metody open z BasePage, podając nasz URL do home page
        self.open(self.HOME_PAGE_URL)


    def open_register_page(self):
        self.open(self.REGISTRATION_PAGE_URL)