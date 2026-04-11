from playwright.sync_api import Page, expect
from pages.playwright.base_page_playwright import BasePagePw


class ProductsPagePw(BasePagePw):
    def __init__(self, page):
        super().__init__(page)

    """ LOKATORY ---"""

    """URL"""
    BIKE_MAIN_LINK = "https://demos.telerik.com/kendo-ui/eshop/Home/Bikes"

    """Kategorie"""
    BIKE_CATEGORY_TITLES = "//div[@class='category-heading']"
    MOUNTAIN_BIKES = "//a[contains(@href, 'subCategory=Mountain Bikes')]"
    ROAD_BIKES = "//a[contains(@href, 'subCategory=Road Bikes')]"
    TOURING_BIKES = "//a[contains(@href, 'subCategory=Touring Bikes')]"

    """ Filtry """
    DISCOUNTED_RADIO = "//input[@type='radio' and @value='2']"
    ALL_BIKES_RADIO = "//input[@name='discountPicker' and @value='1']"
    DISCOUNTED_FILTER = "//label[contains(text(), 'Discounted items only')]"
    ALL_BIKES_FILTER = "//label[contains(text(), 'All')]"

    """ Produkty i Pagery """
    DISCOUNT_BADGE = "//span[@class='discount-pct']"
    PRODUCT_CARD = "//div[contains(@class, 'k-card')]"
    PAGER_INFO = "//span[@class='k-pager-info']"
    PRICE_LABELS = "//div[@class='card-price']"
    PRODUCT_TITLES = "//div[@class='k-card-title']"

    """ Sortowanie """
    SORT_TRIGGER = "//span[contains(@class, 'k-input-value-text')]"
    SORT_LOW_TO_HIGH = "//span[@class='k-list-item-text' and text()='Price - Low to High']"
    SORT_HIGH_TO_LOW = "//span[@class='k-list-item-text' and text()='Price - High to Low']"
    SORT_A_TO_Z = "//span[@class='k-list-item-text' and text()='Name - A to Z']"
    SORT_Z_TO_A = "//span[@class='k-list-item-text' and text()='Name - Z to A']"

    """ Koszyk """
    ADD_TO_CART_BTN = "(//button[contains(@class, 'add-to-cart') or contains(text(), 'Add to Cart')])[1]"
    CART_ICON = "//a[contains(@href, 'Cart')]"
    REMOVE_BTN = "//p[text()='Remove']"
    EMPTY_CART_MSG = "//div[contains(text(), 'Your cart is empty')]"
    CART_TOTAL_PRICE = "//span[@id='subTotalValue']"

    """--- METODY --- """

    def open_main_pw(self):
        self.page.goto(self.BIKE_MAIN_LINK)
        return self

    def open_mountain_bikes_pw(self):
            # 1. Kliknij w link kategorii
            self.page.click(f"xpath={self.MOUNTAIN_BIKES}")

            # 2. ZAMIAST wait_for_url: Czekaj na to, aż lista produktów się zmieni/pojawi
            self.page.wait_for_selector(f"xpath={self.PRODUCT_TITLES}")
            self.page.wait_for_load_state("networkidle")
            return self

    def add_first_product_pw(self):
        self.page.locator(f"xpath={self.ADD_TO_CART_BTN}").click()
        return self

    def go_to_cart_pw(self):
        self.page.click(f"xpath={self.CART_ICON}")
        return self

    def get_all_prices_pw(self):
        locators = self.page.locator(f"xpath={self.PRICE_LABELS}")
        return [float(el.inner_text().replace('$', '').replace(',', '')) for el in locators.all()]

    def get_all_names_pw(self):
        locators = self.page.locator(f"xpath={self.PRODUCT_TITLES}")
        return [el.inner_text().strip() for el in locators.all()]

    def clear_cart_pw(self):
        self.go_to_cart_pw()
        self.page.on("dialog", lambda dialog: dialog.accept())
        while self.page.locator(f"xpath={self.REMOVE_BTN}").count() > 0:
            self.page.locator(f"xpath={self.REMOVE_BTN}").first.click()
        return self

    def filter_discounted_pw(self):
        self.page.click(f"xpath={self.DISCOUNTED_FILTER}")
        return self

    def select_sort_pw(self, xpath_locator):
        self.page.click(f"xpath={self.SORT_TRIGGER}")
        self.page.click(f"xpath={xpath_locator}")
        return self
