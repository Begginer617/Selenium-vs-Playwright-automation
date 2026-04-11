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
    ADD_TO_CART_BTN = "(//button[contains(@class, 'add-to-cart') or contains(text(), 'Add to Cart')])"
    CART_ICON = "//a[contains(@href, 'Cart')]"
    REMOVE_BTN = "//p[text()='Remove']"
    CART_TOTAL_PRICE = "subTotalValue"
    ALL_ADD_BUTTONS = "add-to-cart"

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
        # Użyj .first, aby wskazać, że interesuje Cię tylko pierwszy znaleziony element
        self.page.locator(f"xpath={self.ADD_TO_CART_BTN}").first.click()
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

    def add_multiple_products_and_verify_total_pw(self, count=5):
        print(f"\n[POM] --- Test sumy dla {count} produktów ---")

        # 1. Pobierz ceny wszystkich produktów na stronie
        all_prices = self.get_all_prices_pw()

        if len(all_prices) < count:
            raise Exception(f"BŁĄD: Na stronie znaleziono tylko {len(all_prices)} produktów, a wymagano {count}.")

        # 2. Oblicz sumę oczekiwaną
        selected_prices = all_prices[:count]
        expected_total = sum(selected_prices)
        print(f"[DEBUG] Wybrane ceny: {selected_prices}, Oczekiwana suma: ${expected_total:.2f}")

        # 3. Dodawanie produktów
        add_buttons = self.page.locator(f"xpath={self.ADD_TO_CART_BTN}")

        for i in range(count):
            print(f"[ACTION] Dodaję produkt {i + 1}...")
            add_buttons.nth(i).click()
            self.page.wait_for_timeout(200)  # Czekamy chwilę na dodanie do koszyka

        # 4. Idź do koszyka
        self.go_to_cart_pw()

        # 5. Weryfikacja sumy
        total_element = self.page.locator(f"#{self.CART_TOTAL_PRICE}")  # Zmiana na ID
        expect(total_element).to_be_visible()

        actual_total = float(total_element.inner_text().replace('$', '').replace(',', '').strip())

        print(f"[VERIFY] Suma w koszyku: ${actual_total:.2f}")
        assert round(actual_total, 2) == round(expected_total, 2)
        print("✅ TEST PASSED: Suma w koszyku jest prawidłowa!")