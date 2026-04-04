import time
from selenium.webdriver.common.by import By
from pages.selenium.base_page_selenium import BasePage


class ProductsPage(BasePage):

    '''LINK DO STRONY GŁOWNEJ BIKE'''
    BIKE_MAIN_LINK = "https://demos.telerik.com/kendo-ui/eshop/Home/Bikes"

    '''LOKATORY DO TYPOW ROWEROW'''
    BIKE_CATEGORY_TITLES = (By.XPATH, "//div[@class='category-heading']")
    MOUNTAINS_BIKES_CATEGORY = (By.XPATH, "//a[contains(@href, 'subCategory=Mountain Bikes')]")
    ROAD_BIKES_CATEGORY = (By.XPATH, "//a[contains(@href, 'subCategory=Road Bikes')]")
    TOURING_BIKES_CATEGORY = (By.XPATH, "//a[contains(@href, 'subCategory=Touring Bikes')]")

    def get_bike_category_titles(self):
        elements = self.wait_for_all_visible(self.BIKE_CATEGORY_TITLES)
        return [el.text.strip() for el in elements]

    def open_mountain_bikes(self):
        self.click(self.MOUNTAINS_BIKES_CATEGORY)
        time.sleep(1)  # Chwila na załadowanie produktów

    def open_road_bikes(self):
        self.click(self.ROAD_BIKES_CATEGORY)
        time.sleep(1)  # Chwila na załadowanie produktów

    def open_touring_bikes(self):
        self.click(self.TOURING_BIKES_CATEGORY)
        time.sleep(1) # Chwila na załadowanie produktów

    def open_bikes_main_link(self):
        # najpierw otwórz stronę główną sklepu
        self.open("https://demos.telerik.com/kendo-ui/eshop")
        time.sleep(1)

        # dopiero potem przejdź do Bikes
        self.open(self.BIKE_MAIN_LINK)
        time.sleep(1)

    # --- LOKATORY (Adresy elementów na stronie) ---
    SORT_DROPDOWN_TRIGGER = (By.XPATH, "//span[contains(@class, 'k-input-value-text')]")

    # Opcje wewnątrz dropdowna (tekst musi być identyczny jak na stronie!)
    SORT_FILTER_LOW_TO_HIGH = (By.XPATH, "//span[@class='k-list-item-text' and text()='Price - Low to High']")
    SORT_FILTER_HIGH_TO_LOW = (By.XPATH, "//span[@class='k-list-item-text' and text()='Price - High to Low']")
    SORT_FILTER_A_TO_Z = (By.XPATH, "//span[@class='k-list-item-text' and text()='Name - A to Z']")
    SORT_FILTER_Z_TO_A = (By.XPATH, "//span[@class='k-list-item-text' and text()='Name - Z to A']")

    # --- METODY DO POBIERANIA DANYCH (Twoi "Tłumacze") ---

    def get_all_prices(self):
        """Wyciąga ceny z <div class='card-price'> i zamienia na liczby"""
        # Używamy Twojego lokatora!
        PRICE_LOCATOR = (By.XPATH, "//div[@class='card-price']")

        elements = self.driver.find_elements(*PRICE_LOCATOR)
        prices = []
        for el in elements:
            # Czyścimy tekst "$3,399.99" -> "3399.99"
            clean_text = el.text.replace('$', '').replace(',', '').strip()
            if clean_text:
                prices.append(float(clean_text))
        return prices

    def get_all_names(self):
        """Wyciąga nazwy z <div class='k-card-title'>"""
        # Używamy Twojego lokatora!
        NAME_LOCATOR = (By.XPATH, "//div[@class='k-card-title']")

        elements = self.driver.find_elements(*NAME_LOCATOR)
        return [el.text.strip() for el in elements if el.text]

    # --- GŁÓWNA METODA TESTOWA ---

    def all_sorting_options(self):
        """Pętla, która klika i sprawdza czy Python widzi to samo co strona"""

        sorting_scenarios = [
            (self.SORT_FILTER_A_TO_Z, "name_asc"),
            (self.SORT_FILTER_Z_TO_A, "name_desc"),
            (self.SORT_FILTER_LOW_TO_HIGH, "price_asc"),
            (self.SORT_FILTER_HIGH_TO_LOW, "price_desc")
        ]

        for sorting_option_locator, sort_type in sorting_scenarios:
            # 1. Kliknij dropdown
            self.click(self.SORT_DROPDOWN_TRIGGER)
            time.sleep(0.5)

            # 2. Pobierz nazwę przycisku, żeby wiedzieć co testujemy
            option_name = self.driver.find_element(*sorting_option_locator).text

            # 3. Kliknij w opcję i poczekaj na przeładowanie
            self.click(sorting_option_locator)
            time.sleep(2.0)

            # 4. Sprawdzanie (Asercja)
            if "Price" in option_name:
                actual = self.get_all_prices()
                is_desc = (sort_type == "price_desc")
                expected = sorted(actual, reverse=is_desc)
                assert actual == expected, f"Błąd! Ceny nie są OK dla: {option_name}"

            elif "Name" in option_name:
                actual = self.get_all_names()
                is_desc = (sort_type == "name_desc")
                expected = sorted(actual, reverse=is_desc)
                assert actual == expected, f"Błąd! Nazwy nie są OK dla: {option_name}"

            print(f"✅ Sukces: {option_name} działa poprawnie!")