from playwright.sync_api import Page, expect
from pages.playwright.base_page_playwright import BasePagePw


class ProductsPagePw(BasePagePw):
    def __init__(self, page):
        super().__init__(page)

    """ LOKATORY ---"""
    BIKE_MAIN_LINK = "https://demos.telerik.com/kendo-ui/eshop/Home/Bikes"
    BIKE_CATEGORY_TITLES = "//div[@class='category-heading']"
    MOUNTAIN_BIKES = "//a[contains(@href, 'subCategory=Mountain Bikes')]"
    ROAD_BIKES = "//a[contains(@href, 'subCategory=Road Bikes')]"
    TOURING_BIKES = "//a[contains(@href, 'subCategory=Touring Bikes')]"
    DISCOUNTED_FILTER = "//label[contains(text(), 'Discounted items only')]"
    PRICE_LABELS = "//div[@class='card-price']"
    PRODUCT_TITLES = "//div[@class='k-card-title']"
    SORT_TRIGGER = "//span[contains(@class, 'k-input-value-text')]"
    ADD_TO_CART_BTN = "(//button[contains(@class, 'add-to-cart') or contains(text(), 'Add to Cart')])[1]"
    CART_ICON = "//a[contains(@href, 'Cart')]"
    REMOVE_BTN = "//p[text()='Remove']"

    """--- METODY --- """

    def open_main_pw(self):
        print(f"[POM] Nawiguję do strony: {self.BIKE_MAIN_LINK}")
        self.page.goto(self.BIKE_MAIN_LINK)
        return self

    def open_mountain_bikes_pw(self):
        print(f"[POM] Klikam kategorię: Mountain Bikes")
        self.page.click(f"xpath={self.MOUNTAIN_BIKES}")
        self.page.wait_for_selector(f"xpath={self.PRODUCT_TITLES}")
        self.page.wait_for_load_state("networkidle")
        return self

    def add_first_product_pw(self):
        print(f"[POM] Klikam przycisk 'Add to Cart' dla pierwszego produktu")
        self.page.locator(f"xpath={self.ADD_TO_CART_BTN}").click()
        return self

    def add_first_product_to_cart_and_verify_pw(self):
        product_names = self.get_all_names_pw()
        first_product_name = product_names[0]
        print(f"[INFO] Wybrany produkt: '{first_product_name}'")

        print(f"[ACTION] Dodaję produkt do koszyka...")
        self.add_first_product_pw()

        print(f"[ACTION] Przechodzę do koszyka...")
        self.go_to_cart_pw()

        print(f"[VERIFY] Sprawdzam czy '{first_product_name}' jest w koszyku...")
        cart_item_locator = self.page.locator(f"//*[contains(text(), '{first_product_name}')]")

        expect(cart_item_locator.first).to_be_visible()
        print(f"[SUCCESS] Element znaleziony w koszyku!")

        expect(cart_item_locator.first).to_contain_text(first_product_name)
        print(f"✅ TEST PASSED: Nazwa produktu w koszyku się zgadza.")
        return self

    def go_to_cart_pw(self):
        print(f"[POM] Klikam ikonę koszyka")
        self.page.click(f"xpath={self.CART_ICON}")
        return self

    def get_all_prices_pw(self):
        print(f"[POM] Pobieram ceny produktów")
        locators = self.page.locator(f"xpath={self.PRICE_LABELS}")
        return [float(el.inner_text().replace('$', '').replace(',', '')) for el in locators.all()]

    def get_all_names_pw(self):
        print(f"[POM] Pobieram nazwy produktów")
        locators = self.page.locator(f"xpath={self.PRODUCT_TITLES}")
        return [el.inner_text().strip() for el in locators.all()]

    def clear_cart_pw(self):
        print(f"[POM] Rozpoczynam czyszczenie koszyka...")
        self.go_to_cart_pw()
        self.page.on("dialog", lambda dialog: dialog.accept())
        while self.page.locator(f"xpath={self.REMOVE_BTN}").count() > 0:
            print(f"[POM] Usuwam element...")
            self.page.locator(f"xpath={self.REMOVE_BTN}").first.click()
        print(f"[POM] Koszyk jest pusty.")
        return self

    def filter_discounted_pw(self):
        print(f"[POM] Filtruję produkty przecenione")
        self.page.click(f"xpath={self.DISCOUNTED_FILTER}")
        return self

    def select_sort_pw(self, xpath_locator):
        print(f"[POM] Zmieniam sortowanie...")
        self.page.click(f"xpath={self.SORT_TRIGGER}")
        self.page.click(f"xpath={xpath_locator}")
        return self