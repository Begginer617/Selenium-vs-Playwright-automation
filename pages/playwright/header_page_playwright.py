from playwright.sync_api import Page

class HeaderPagePw:
    def __init__(self, page: Page):
        self.page = page
        # Używamy dokładnie Twoich sprawdzonych lokatorów
        self.SHOPPING_CART_BTN = "//a[contains(@href, 'ShoppingCart')]"
        self.CATEGORIES_MENU = "//span[normalize-space()='Categories']"
        self.ACCESSORIES_LINK = "//a[contains(@class, 'k-menu-link') and normalize-space()='Accessories']"
        self.BIKES_LINK = "//a[contains(@class, 'k-menu-link') and normalize-space()='Bikes']"
        self.CLOTHES_LINK = "//a[contains(@class, 'k-menu-link') and normalize-space()='Clothes']"
        self.COMPONENTS_LINK = "//a[contains(@class, 'k-menu-link') and normalize-space()='Components']"

    def click_cart_pw(self):
        self.page.locator(self.SHOPPING_CART_BTN).click()

    def open_home_page_pw(self):
        self.page.goto("https://demos.telerik.com/kendo-ui/eshop")

    def get_url_pw(self):
        return self.page.url

    # Metody z Twoją logiką hovera
    def _hover_menu_pw(self):
        # Dodajemy .first, aby wybrać pierwszy z dwóch znalezionych elementów
        self.page.locator(self.CATEGORIES_MENU).first.hover()

    def open_accessories_category_pw(self):
        self._hover_menu_pw()
        self.page.locator(self.ACCESSORIES_LINK).click()

    def open_bikes_category_pw(self):
        self._hover_menu_pw()
        self.page.locator(self.BIKES_LINK).click()

    def open_clothes_category_pw(self):
        self._hover_menu_pw()
        self.page.locator(self.CLOTHES_LINK).click()

    def open_components_category_pw(self):
        self._hover_menu_pw()
        self.page.locator(self.COMPONENTS_LINK).click()