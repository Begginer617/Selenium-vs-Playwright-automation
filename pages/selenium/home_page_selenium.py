from pages.selenium.base_page_selenium import BasePage

class HomePage(BasePage):
    # Zmienna klasowa z adresem
    URL = "https://demos.telerik.com/kendo-ui/eshop/"

    def open_home_page(self):
        # Używamy metody open z BasePage, podając nasz URL
        self.open(self.URL)