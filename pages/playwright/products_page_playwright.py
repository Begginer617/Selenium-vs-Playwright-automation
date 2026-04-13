from playwright.sync_api import Page, expect
from pages.playwright.base_page_playwright import BasePagePw


class ProductPagePw(BasePagePw):
    def __init__(self, page):
        super().__init__(page)

    """ LOKATORY ---"""
    BIKE_MAIN_LINK = "https://demos.telerik.com/kendo-ui/eshop/Home/Bikes"
    BIKE_CATEGORY_TITLES = "//div[@class='category-heading']"
    MOUNTAIN_BIKES = "//a[contains(@href, 'subCategory=Mountain Bikes')]"
    PRODUCT_TITLES = "//div[@class='k-card-title']"
    ROAD_BIKES = "//a[contains(@href, 'subCategory=Road Bikes')]"
    TOURING_BIKES = "//a[contains(@href, 'subCategory=Touring Bikes')]"

    ALL_BIKES_FILTER = "//label[contains(text(), 'All')]"
    DISCOUNTED_BIKES_FILTER = "//label[contains(text(), 'Discounted items only')]"

    # Pager i karty
    PAGER_INFO = "//span[contains(@class, 'k-pager-info')]"
    PRODUCT_CARDS = "//div[contains(@class, 'k-card') and not(contains(@class, 'k-card-list'))]"
    DISCOUNT_BADGE = "//span[@class='discount-pct']"

    # Sortowanie
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



    """--- METODY ---"""

    def open_bikes_main_link_pw(self):
        print(f"[POM] Nawiguję do strony głównej rowerów: {self.BIKE_MAIN_LINK}")
        self.page.goto(self.BIKE_MAIN_LINK)
        return self

    def get_bike_category_titles_pw(self):
        print("[POM] Pobieram tytuły kategorii rowerów...")
        titles = self.page.locator(self.BIKE_CATEGORY_TITLES).all_inner_texts()
        return titles

    def open_mountain_bikes_pw(self):
        print("[POM] Klikam kategorię: Mountain Bikes")
        self.page.locator(self.MOUNTAIN_BIKES).first.click()
        self.page.wait_for_load_state("networkidle")
        return self

    def click_filter_all_pw(self):
        print("[POM] Nakładam filtr: All")
        self.page.locator(self.ALL_BIKES_FILTER).click()
        self.page.wait_for_timeout(1000)
        return self

    def click_filter_discounted_pw(self):
        print("[POM] Nakładam filtr: Discounted items only")
        self.page.locator(self.DISCOUNTED_BIKES_FILTER).click()
        self.page.wait_for_timeout(1000)
        return self

    def get_total_count_from_pager_pw(self):
        print("[POM] Odczytuję liczbę produktów z pagera...")

        # Czekamy, aż pager w ogóle się pojawi (max 5s, żeby nie marnować czasu)
        self.page.wait_for_selector(self.PAGER_INFO, state="visible", timeout=5000)

        # Pobieramy tekst
        text = self.page.locator(self.PAGER_INFO).inner_text()

        # Debugging: jeśli znowu się wywali, zobaczysz w logach co tam właściwie było
        print(f"[DEBUG] Tekst pagera: '{text}'")

        count = int(text.split("of")[-1].strip().split(" ")[0])
        print(f"[DEBUG] Wartość z pagera: {count}")
        return count

    def count_badges_pw(self):
        # Upewniamy się, że czekamy na plakietki po załadowaniu filtra
        # Czekamy aż pojawi się przynajmniej jedna plakietka
        self.page.wait_for_selector(self.DISCOUNT_BADGE, state="visible", timeout=5000)
        count = self.page.locator(self.DISCOUNT_BADGE).count()
        print(f"[POM] Liczba znalezionych plakietek rabatowych: {count}")
        return count

    def debug_page_content_pw(self):
        # Pobierz teksty wszystkich plakietek, jakie uda się znaleźć na stronie
        all_badges = self.page.locator("//span[contains(@class, 'k-badge')]").all_inner_texts()
        print(f"[DEBUG] Znalezione plakietki na stronie: {all_badges}")

    def count_visible_bikes_pw(self):
        # Zliczamy tylko te karty, które są widoczne (nie mają display: none)
        count = self.page.locator(self.PRODUCT_CARDS).filter(has_not=self.page.locator("text='hidden'")).count()
        # Lub po prostu wymuś czekanie na widoczność:
        count = self.page.locator(self.PRODUCT_CARDS).filter(has=self.page.locator(".discount-pct")).count()
        print(f"[POM] Liczba widocznych kart produktów: {count}")
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
