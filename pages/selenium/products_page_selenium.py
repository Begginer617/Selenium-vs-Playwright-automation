import time
from selenium.webdriver.common.by import By
from pages.selenium.base_page_selenium import BasePage


class ProductsPage(BasePage):
    """KONSTANTY I LINKI"""
    BIKE_MAIN_LINK = "https://demos.telerik.com/kendo-ui/eshop/Home/Bikes"

    """# --- LOKATORY: KATEGORIE ---"""
    BIKE_CATEGORY_TITLES = (By.XPATH, "//div[@class='category-heading']")
    MOUNTAINS_BIKES_CATEGORY = (By.XPATH, "//a[contains(@href, 'subCategory=Mountain Bikes')]")
    ROAD_BIKES_CATEGORY = (By.XPATH, "//a[contains(@href, 'subCategory=Road Bikes')]")
    TOURING_BIKES_CATEGORY = (By.XPATH, "//a[contains(@href, 'subCategory=Touring Bikes')]")

    """# --- LOKATORY: FILTRY ---"""
    # Radio Buttony (do sprawdzania stanu)
    DISCOUNTED_BIKES_RADIO_BUTTON = (By.XPATH, "//input[@type='radio' and @value='2']")
    ALL_BIKES_RADIO_BUTTON = (By.XPATH, "//input[@name='discountPicker' and @value='1']")

    """# Etykiety (do klikania)"""
    DISCOUNTED_BIKES_FILTER = (By.XPATH, "//label[contains(text(), 'Discounted items only')]")
    ALL_BIKES_FILTER = (By.XPATH, "//label[contains(text(), 'All')]")

    """# Elementy na karcie produktu"""
    DISCOUNT_PERCENT_BADGE = (By.XPATH, "//span[@class='discount-pct']")
    PRODUCT_CARD = (By.XPATH, "//div[contains(@class, 'k-card')]")
    PAGER_INFO = (By.XPATH, "//span[@class='k-pager-info']")

    """# --- LOKATORY: SORTOWANIE ---"""
    SORT_DROPDOWN_TRIGGER = (By.XPATH, "//span[contains(@class, 'k-input-value-text')]")
    SORT_FILTER_LOW_TO_HIGH = (By.XPATH, "//span[@class='k-list-item-text' and text()='Price - Low to High']")
    SORT_FILTER_HIGH_TO_LOW = (By.XPATH, "//span[@class='k-list-item-text' and text()='Price - High to Low']")
    SORT_FILTER_A_TO_Z = (By.XPATH, "//span[@class='k-list-item-text' and text()='Name - A to Z']")
    SORT_FILTER_Z_TO_A = (By.XPATH, "//span[@class='k-list-item-text' and text()='Name - Z to A']")

    """# --- LOKATORY: KOSZYK ---"""
    # Przycisk "Add to Cart" na karcie produktu (pierwszy z brzegu)
    ADD_TO_CART_BUTTON = (By.XPATH, "(//button[contains(@class, 'add-to-cart') or contains(text(), 'Add to Cart')])[1]")

    # Ikona koszyka/przycisk przejścia do koszyka
    CART_ICON = (By.XPATH, "//a[contains(@href, 'Cart')]")

    # Elementy wewnątrz koszyka
    CART_ITEM_TITLES = (By.CSS_SELECTOR, ".cart-item-name, .k-card-title, .product-name")

    # Przycisk usuwania w koszyku (wszystkie widoczne)
    REMOVE_ITEM_BUTTONS = (By.XPATH, "//p[text()='Remove']")
    # Tekst informujący o pustym koszyku (opcjonalnie)
    EMPTY_CART_MESSAGE = (By.XPATH, "//div[contains(text(), 'Your cart is empty')]")

    CART_TOTAL_PRICE = (By.ID, "subTotalValue")
    ALL_ADD_BUTTONS = (By.CLASS_NAME, "add-to-cart")


    """# --- Metody: KOSZYK ---"""

    def add_first_product_to_cart_and_verify(self):
        """Dodaje pierwszy produkt do koszyka i sprawdza czy tam jest"""
        # 1. Pobierz nazwę pierwszego produktu
        product_name = self.get_all_names()[0]
        print(f"Próbuję dodać: {product_name}")

        # 2. Kliknij Add to Cart
        self.click(self.ADD_TO_CART_BUTTON)
        time.sleep(2)  # Kendo potrzebuje chwili na animację "fly-to-cart"

        # 3. Przejdź do koszyka
        self.click(self.CART_ICON)
        # Czekamy aż URL się zmieni na /Cart lub pojawi się kontener koszyka
        self.wait_for_page_load(3)

        # 4. Sprawdź czy nazwa w koszyku się zgadza
        CART_ITEM_TITLES = (By.CSS_SELECTOR, ".cart-item-name, .k-card-title, .product-name")

        # Używamy wait_for_all_visible zamiast find_elements, żeby uniknąć pustej listy []
        try:
            elements = self.wait_for_all_visible(CART_ITEM_TITLES)
            cart_names = [el.text.strip() for el in elements]
        except:
            cart_names = []

        print(f"Znalezione w koszyku: {cart_names}")

        assert product_name in cart_names, f"BŁĄD: Produktu {product_name} nie ma w koszyku! Znaleziono: {cart_names}"

    def add_multiple_products_and_verify_total(self, count=5):
        """Dodaje X produktów i weryfikuje sumę cen w koszyku"""
        print(f"\n--- Test sumy dla {count} produktów ---")

        all_prices = self.get_all_prices()
        # Wybieramy pierwsze 'count' produktów z listy
        selected_prices = all_prices[:count]
        expected_total = sum(selected_prices)

        # Dodawanie produktów
        add_buttons = self.driver.find_elements(*self.ALL_ADD_BUTTONS)
        for i in range(count):
            print(f"Dodaję produkt {i + 1} o cenie: ${selected_prices[i]}")
            add_buttons[i].click()
            time.sleep(1)

        # Idź do koszyka
        self.click(self.CART_ICON)

        # CZEKANIE: Zamiast driver.find_element, używamy metody z BasePage (jeśli ją masz)
        # lub bezpośrednio WebDriverWait
        print("Czekam na przeliczenie sumy w koszyku...")
        time.sleep(2)  # Prosty sleep na początek, żeby sprawdzić czy to kwestia czasu

        try:
            # Szukamy elementu sumy
            total_element = self.driver.find_element(*self.CART_TOTAL_PRICE)
            actual_total_text = total_element.text
            print(f"Pobrany tekst sumy: '{actual_total_text}'")

            # Konwersja "$1,234.56" -> 1234.56
            actual_total = float(actual_total_text.replace('$', '').replace(',', '').strip())
        except Exception as e:
            # Jeśli padnie, zrób zrzut nazw klas dostępnych na stronie, żebyśmy wiedzieli co jest nie tak
            print(f"Nie udało się pobrać sumy. Błąd: {e}")
            raise

        print(f"Suma oczekiwana: ${expected_total:.2f}")
        print(f"Suma w koszyku: ${actual_total:.2f}")

        # Używamy round(), bo floaty w Pythonie bywają kapryśne (np. 0.1 + 0.2 != 0.3)
        assert round(actual_total, 2) == round(expected_total, 2), \
            f"BŁĄD SUMY! Jest {actual_total}, powinno być {expected_total}"
        print("✅ Suma w koszyku jest prawidłowa!")

    def clear_cart(self):
        """Pancerny sposób na wyczyszczenie koszyka z obsługą Alertów"""
        print("\n--- Rozpoczynam czyszczenie koszyka ---")
        self.click(self.CART_ICON)
        time.sleep(2)

        while True:
            # Pobieramy świeżą listę guzików
            buttons = self.driver.find_elements(By.CLASS_NAME, "remove-product")

            if not buttons:
                print("Koszyk jest pusty.")
                break

            print(f"Usuwam produkt... (Zostało: {len(buttons)})")
            try:
                buttons[0].click()
                time.sleep(1)  # Czekamy ułamek sekundy na pojawienie się alertu

                # --- KLUCZOWY MOMENT: Obsługa Alertu ---
                alert = self.driver.switch_to.alert
                print(f"Akceptuję alert: {alert.text}")
                alert.accept()

                # Czekamy na przeładowanie się koszyka po usunięciu
                time.sleep(1.5)
            except Exception as e:
                print(f"Koniec usuwania lub brak alertu: {e}")
                break

        print("Czyszczenie zakończone. Wracam na stronę główną.")
        self.open_bikes_main_link()



    """# --- METODY: NAWIGACJA ---"""

    def open_bikes_main_link(self):
        """Otwiera stronę główną rowerów"""
        self.open("https://demos.telerik.com/kendo-ui/eshop")
        time.sleep(1)
        self.open(self.BIKE_MAIN_LINK)
        time.sleep(1)

    def open_mountain_bikes(self):
        """Wchodzi w kategorię Mountain Bikes"""
        self.click(self.MOUNTAINS_BIKES_CATEGORY)
        time.sleep(2)

    """# --- METODY: POBIERANIE DANYCH (GETTERS) ---"""

    def get_all_prices(self):
        """Pobiera wszystkie ceny i zamienia na float"""
        PRICE_LOCATOR = (By.XPATH, "//div[@class='card-price']")
        elements = self.driver.find_elements(*PRICE_LOCATOR)
        prices = []
        for el in elements:
            clean_text = el.text.replace('$', '').replace(',', '').strip()
            if clean_text:
                prices.append(float(clean_text))
        return prices

    def get_all_names(self):
        """Pobiera wszystkie nazwy produktów"""
        NAME_LOCATOR = (By.XPATH, "//div[@class='k-card-title']")
        elements = self.driver.find_elements(*NAME_LOCATOR)
        return [el.text.strip() for el in elements if el.text]

    def get_all_discount_labels(self):
        """Pobiera teksty z plakietek rabatowych (np. '20% off')"""
        elements = self.driver.find_elements(*self.DISCOUNT_PERCENT_BADGE)
        return [el.text.strip() for el in elements if el.text]

    def get_total_count_from_pager(self):
        """Wyciąga łączną liczbę przedmiotów z pagera (np. 32)"""
        text_info = self.driver.find_element(*self.PAGER_INFO).text
        # Split: ['1', '-', '12', 'of', '32', 'items'] -> bierzemy index 4
        parts = text_info.split()
        return int(parts[4])

    def get_bike_category_titles(self):
        """Pobiera teksty z nagłówków kategorii (Mountain, Road, Touring)"""
        elements = self.wait_for_all_visible(self.BIKE_CATEGORY_TITLES)
        return [el.text.strip() for el in elements]

    """# --- METODY: LICZENIE (COUNTERS) ---"""

    def count_visible_bikes(self):
        """Zlicza kafelki, które mają widoczny tekst tytułu"""
        # Szukamy tytułów wewnątrz kart
        titles = self.driver.find_elements(By.XPATH, "//div[contains(@class, 'k-card')]//div[@class='k-card-title']")

        # Liczymy tylko te, które faktycznie mają jakiś tekst (nie są puste)
        visible_titles = [t for t in titles if t.text.strip() != ""]

        return len(visible_titles)

    def count_badges(self):
        """Zlicza plakietki procentowe widoczne na ekranie"""
        return len(self.get_all_discount_labels())

    """# --- METODY: TESTOWE (AKCJE I WERYFIKACJA) ---"""

    def verify_discount_filter(self):
        """KLUCZOWY TEST: Sprawdza czy filtr rabatów działa uczciwie"""
        print("Aktywuję filtr: Discounted items only...")
        self.click(self.DISCOUNTED_BIKES_FILTER)
        time.sleep(2)  # Czekamy na przeładowanie listy

        bikes_count = self.count_visible_bikes()
        badges_count = self.count_badges()

        print(f"DEBUG: Znaleziono {bikes_count} produktów i {badges_count} plakietek.")

        assert bikes_count > 0, "BŁĄD: Filtr nie zwrócił żadnych wyników!"
        assert bikes_count == badges_count, (
            f"BŁĄD FILTRA! Wyświetlono {bikes_count} produktów, "
            f"ale tylko {badges_count} ma plakietkę rabatu."
        )
        print("✅ SUKCES: Wszystkie widoczne produkty posiadają rabat.")

    def all_sorting_options(self):
        """Testuje po kolei wszystkie opcje sortowania"""
        scenarios = [
            (self.SORT_FILTER_A_TO_Z, "name_asc"),
            (self.SORT_FILTER_Z_TO_A, "name_desc"),
            (self.SORT_FILTER_LOW_TO_HIGH, "price_asc"),
            (self.SORT_FILTER_HIGH_TO_LOW, "price_desc")
        ]

        for locator, sort_type in scenarios:
            self.click(self.SORT_DROPDOWN_TRIGGER)
            time.sleep(0.5)

            option_name = self.driver.find_element(*locator).text
            self.click(locator)
            time.sleep(2)

            if "Price" in option_name:
                actual = self.get_all_prices()
                is_desc = (sort_type == "price_desc")
                assert actual == sorted(actual, reverse=is_desc), f"Błąd sortowania cen: {option_name}"
            elif "Name" in option_name:
                actual = self.get_all_names()
                is_desc = (sort_type == "name_desc")
                assert actual == sorted(actual, reverse=is_desc), f"Błąd sortowania nazw: {option_name}"

            print(f"✅ Sukces: Sortowanie '{option_name}' działa poprawnie!")