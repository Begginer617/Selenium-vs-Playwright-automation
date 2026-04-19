from playwright.sync_api import Page, expect
from pages.playwright.base_page_playwright import BasePagePw


class ProductPagePw(BasePagePw):
    def __init__(self, page):
        super().__init__(page)

    """LOCATORS"""
    BIKE_MAIN_LINK = "https://demos.telerik.com/kendo-ui/eshop/Home/Bikes"
    BIKE_CATEGORY_TITLES = "//div[@class='category-heading']"
    MOUNTAIN_BIKES = "//a[contains(@href, 'subCategory=Mountain Bikes')]"
    PRODUCT_TITLES = "//div[@class='k-card-title']"
    ROAD_BIKES = "//a[contains(@href, 'subCategory=Road Bikes')]"
    TOURING_BIKES = "//a[contains(@href, 'subCategory=Touring Bikes')]"

    ALL_BIKES_FILTER = "//label[contains(text(), 'All')]"
    DISCOUNTED_BIKES_FILTER = "//label[contains(text(), 'Discounted items only')]"

    # Pager and cards
    PAGER_INFO = "//span[contains(@class, 'k-pager-info')]"
    PRODUCT_CARDS = "//div[contains(@class, 'k-card') and not(contains(@class, 'k-card-list'))]"
    DISCOUNT_BADGE = "//span[@class='discount-pct']"

    # Sorting
    SORT_TRIGGER = "//span[contains(@class, 'k-input-value-text')]"
    SORT_OPTION_PRICE_DESC = "text=Price - High to Low"
    SORT_OPTION_PRICE_ASC = "text=Price - Low to High"
    CART_ICON = "//a[contains(@href, 'Cart')]"
    REMOVE_BTN = "//p[text()='Remove']"
    DISCOUNTED_FILTER = "//label[contains(text(), 'Discounted items only')]"
    PRICE_LABELS = "//div[@class='card-price']"
    ADD_TO_CART_BTN = "(//button[contains(@class, 'add-to-cart') or contains(text(), 'Add to Cart')])"
    CART_TOTAL_PRICE = "subTotalValue"
    ALL_ADD_BUTTONS = "add-to-cart"



    """ACTIONS AND ASSERTIONS"""

    def open_bikes_main_link_pw(self):
        print(f"[POM] Navigating to bikes landing page: {self.BIKE_MAIN_LINK}")
        self.page.goto(self.BIKE_MAIN_LINK)
        return self

    def get_bike_category_titles_pw(self):
        print("[POM] Collecting bike category titles...")
        return self.page.locator(self.BIKE_CATEGORY_TITLES).all_inner_texts()

    def open_mountain_bikes_pw(self):
        print("[POM] Opening category: Mountain Bikes")
        self.page.locator(self.MOUNTAIN_BIKES).first.click()
        self.page.wait_for_load_state("networkidle")
        return self

    def click_filter_all_pw(self):
        print("[POM] Applying filter: All")
        self.page.locator(self.ALL_BIKES_FILTER).click()
        self.page.wait_for_timeout(1000)
        return self

    def click_filter_discounted_pw(self):
        print("[POM] Applying filter: Discounted items only")
        self.page.locator(self.DISCOUNTED_BIKES_FILTER).click()
        self.page.wait_for_timeout(1000)
        return self

    def get_total_count_from_pager_pw(self):
        print("[POM] Reading product count from pager...")
        self.page.wait_for_selector(self.PAGER_INFO, state="visible", timeout=5000)
        text = self.page.locator(self.PAGER_INFO).inner_text()
        print(f"[DEBUG] Pager text: '{text}'")
        count = int(text.split("of")[-1].strip().split(" ")[0])
        print(f"[DEBUG] Parsed pager count: {count}")
        return count

    def assert_expected_bike_categories_pw(self, expected_titles=None):
        titles = self.get_bike_category_titles_pw()
        print(f"[POM] Bike categories found: {titles}")
        expected_titles = expected_titles or ["Mountain Bikes", "Road Bikes", "Touring Bikes"]
        for expected in expected_titles:
            assert expected in titles, f"Expected category '{expected}' in {titles}"

    def assert_products_available_for_all_filter_pw(self):
        self.click_filter_all_pw()
        all_count = self.get_total_count_from_pager_pw()
        assert all_count > 0, f"Expected products for 'All' filter, got count={all_count}"
        return all_count

    def assert_discount_filter_consistency_pw(self, expected_all_count=None):
        self.click_filter_discounted_pw()
        actual_discounted_pager = self.get_total_count_from_pager_pw()
        actual_badges = self.count_badges_pw()
        visible_cards = self.count_visible_bikes_pw()
        if expected_all_count is not None:
            assert actual_discounted_pager <= expected_all_count, (
                f"Discounted pager count ({actual_discounted_pager}) should not exceed all-items count "
                f"({expected_all_count})."
            )
        assert actual_discounted_pager > 0, "Discount filter should return at least one product."
        assert actual_badges == actual_discounted_pager, (
            f"Discount badge count ({actual_badges}) should match pager count ({actual_discounted_pager})."
        )
        assert visible_cards == actual_discounted_pager, (
            f"Visible discounted cards ({visible_cards}) should match pager count ({actual_discounted_pager})."
        )

    def assert_filter_counts_consistent_pw(self):
        all_count = self.assert_products_available_for_all_filter_pw()
        self.assert_discount_filter_consistency_pw(expected_all_count=all_count)

    def count_badges_pw(self):
        self.page.wait_for_selector(self.DISCOUNT_BADGE, state="visible", timeout=5000)
        count = self.page.locator(self.DISCOUNT_BADGE).count()
        print(f"[POM] Discount badge count: {count}")
        return count

    def debug_page_content_pw(self):
        all_badges = self.page.locator("//span[contains(@class, 'k-badge')]").all_inner_texts()
        print(f"[DEBUG] Badges visible on page: {all_badges}")

    def count_visible_bikes_pw(self):
        count = self.page.locator(self.PRODUCT_CARDS).filter(has=self.page.locator(".discount-pct")).count()
        print(f"[POM] Visible discounted cards count: {count}")
        return count

    def clear_cart_pw(self):
        print(f"[POM] Rozpoczynam czyszczenie koszyka...")
        self.go_to_cart_pw()
        self.page.on("dialog", lambda dialog: dialog.accept())
        while self.page.locator(f"xpath={self.REMOVE_BTN}").count() > 0:
            print(f"[POM] Usuwam element...")
            self.page.locator(f"xpath={self.REMOVE_BTN}").first.click()
        print(f"[POM] Koszyk jest pusty.")
        return self


    def go_to_cart_pw(self):
        print(f"[POM] Klikam ikonę koszyka")
        self.page.click(f"xpath={self.CART_ICON}")
        return self

    def add_first_product_pw(self):
        print(f"[POM] Klikam przycisk 'Add to Cart' dla pierwszego produktu")
        # Użyj .first, aby wskazać, że interesuje Cię tylko pierwszy znaleziony element
        self.page.locator(f"xpath={self.ADD_TO_CART_BTN}").first.click()
        return self

    def get_all_prices_pw(self):
        print(f"[POM] Pobieram ceny produktów")
        locators = self.page.locator(f"xpath={self.PRICE_LABELS}")
        return [float(el.inner_text().replace('$', '').replace(',', '')) for el in locators.all()]

    def get_all_names_pw(self):
        print(f"[POM] Pobieram nazwy produktów")
        locators = self.page.locator(f"xpath={self.PRODUCT_TITLES}")
        return [el.inner_text().strip() for el in locators.all()]

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

    def all_sorting_options_pw(self):
        print("\n[POM] --- Start sekwencji sortowania ---")

        # 1. Klikamy trigger, żeby otworzyć menu
        self.page.locator(self.SORT_TRIGGER).click()

        # 2. Czekamy na element listy (li), a nie na span
        # Wybieramy opcję: Price - High to Low
        self.page.locator("li[role='option']:has-text('Price - High to Low')").click()

        print("[ACTION] Wybrano: Price - High to Low")
        self.page.wait_for_timeout(1000)

        # 3. Ponownie klikamy trigger
        self.page.locator(self.SORT_TRIGGER).click()

        # Wybieramy opcję: Price - Low to High
        self.page.locator("li[role='option']:has-text('Price - Low to High')").click()

        print("[ACTION] Wybrano: Price - Low to High")
        self.page.wait_for_timeout(1000)

        print("[POM] --- Koniec sekwencji sortowania ---")

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
