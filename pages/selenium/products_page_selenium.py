import re
import time

import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait

from pages.selenium.base_page_selenium import BasePage


class ProductsPage(BasePage):
    """Constants and links."""
    BIKE_MAIN_LINK = "https://demos.telerik.com/kendo-ui/eshop/Home/Bikes"

    """Category locators."""
    BIKE_CATEGORY_TITLES = (By.XPATH, "//div[@class='category-heading']")
    MOUNTAINS_BIKES_CATEGORY = (By.XPATH, "//a[contains(@href, 'subCategory=Mountain Bikes')]")
    ROAD_BIKES_CATEGORY = (By.XPATH, "//a[contains(@href, 'subCategory=Road Bikes')]")
    TOURING_BIKES_CATEGORY = (By.XPATH, "//a[contains(@href, 'subCategory=Touring Bikes')]")

    """Filter locators."""
    # Radio buttons (state checks)
    DISCOUNTED_BIKES_RADIO_BUTTON = (By.XPATH, "//input[@type='radio' and @value='2']")
    ALL_BIKES_RADIO_BUTTON = (By.XPATH, "//input[@name='discountPicker' and @value='1']")

    """Filter labels (click targets)."""
    DISCOUNTED_BIKES_FILTER = (By.XPATH, "//label[contains(text(), 'Discounted items only')]")
    ALL_BIKES_FILTER = (By.XPATH, "//label[contains(text(), 'All')]")

    """Product card elements."""
    DISCOUNT_PERCENT_BADGE = (By.XPATH, "//span[@class='discount-pct']")
    PRODUCT_CARD = (By.XPATH, "//div[contains(@class, 'k-card')]")
    PAGER_INFO = (By.XPATH, "//span[@class='k-pager-info']")

    """Sorting locators."""
    SORT_DROPDOWN_TRIGGER = (By.XPATH, "//span[contains(@class, 'k-input-value-text')]")
    SORT_FILTER_LOW_TO_HIGH = (By.XPATH, "//span[@class='k-list-item-text' and text()='Price - Low to High']")
    SORT_FILTER_HIGH_TO_LOW = (By.XPATH, "//span[@class='k-list-item-text' and text()='Price - High to Low']")
    SORT_FILTER_A_TO_Z = (By.XPATH, "//span[@class='k-list-item-text' and text()='Name - A to Z']")
    SORT_FILTER_Z_TO_A = (By.XPATH, "//span[@class='k-list-item-text' and text()='Name - Z to A']")

    """Cart locators."""
    # "Add to Cart" on the first product card
    ADD_TO_CART_BUTTON = (By.XPATH, "(//button[contains(@class, 'add-to-cart') or contains(text(), 'Add to Cart')])[1]")

    # Cart icon / navigation button
    CART_ICON = (By.XPATH, "//a[contains(@href, 'Cart')]")

    # Elements inside cart
    CART_ITEM_TITLES = (By.CSS_SELECTOR, ".cart-item-name, .k-card-title, .product-name")

    # Remove actions in cart (supports text/button variants).
    REMOVE_ITEM_BUTTONS = (By.CSS_SELECTOR, ".remove-product")
    # Optional empty-cart message (text differs slightly across UI variants).
    EMPTY_CART_MESSAGE = (
        By.XPATH,
        "//*[contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'cart is empty')]",
    )

    CART_LINE_ITEM_PRICES = (
        By.XPATH,
        "//td[contains(@class, 'final-price')] | //span[contains(@class, 'card-price')]"
    )

    CART_TOTAL_PRICE = (By.ID, "subTotalValue")
    ALL_ADD_BUTTONS = (By.CLASS_NAME, "add-to-cart")


    """Cart actions."""

    def add_first_product_to_cart_and_verify(self):
        """Add first product to cart and verify it is present."""
        # 1. Capture first product name
        product_name = self.get_all_names()[0]
        self.log_info(f"Trying to add product: {product_name}")

        # 2. Click Add to Cart
        previous_count = self._current_cart_count()
        self.click(self.ADD_TO_CART_BUTTON)
        time.sleep(0.2)

        # 3. Open cart
        self.click(self.CART_ICON)
        self.wait_for_url("Cart", timeout=6)
        self._wait(
            lambda d: len(d.find_elements(*self.CART_ITEM_TITLES)) > 0
            or len(d.find_elements(*self.EMPTY_CART_MESSAGE)) > 0,
            timeout=4,
        )

        # 4. Verify product name inside cart
        CART_ITEM_TITLES = (By.CSS_SELECTOR, ".cart-item-name, .k-card-title, .product-name")

        # Use explicit visibility wait to avoid unstable empty-list reads.
        try:
            elements = self.wait_for_all_visible(CART_ITEM_TITLES, timeout=4)
            cart_names = [el.text.strip() for el in elements]
        except:
            cart_names = []

        self.log_info(f"Cart items found: {cart_names}")

        assert product_name in cart_names, (
            f"ERROR: Product '{product_name}' not found in cart. Found: {cart_names}"
        )

    def add_multiple_products_and_verify_total(self, count=5):
        """Add N products and verify total cart value."""
        self.log_step(f"Starting cart total validation for {count} products")
        selected_prices = []

        # Add products
        for i in range(count):
            # Re-fetch buttons each loop because product cards are re-rendered after add-to-cart.
            current_add_buttons = self.driver.find_elements(*self.ALL_ADD_BUTTONS)
            current_prices = self.get_all_prices()
            if i >= len(current_add_buttons):
                raise AssertionError(
                    f"Could not find add-to-cart button for product index {i}. "
                    f"Only {len(current_add_buttons)} buttons found."
                )
            if i >= len(current_prices):
                raise AssertionError(
                    f"Could not read price for product index {i}. "
                    f"Only {len(current_prices)} prices found."
                )
            selected_prices.append(current_prices[i])
            self.log_step(f"Adding product #{i + 1} priced at ${selected_prices[i]}")
            previous_count = self._current_cart_count()
            current_add_buttons[i].click()
            try:
                self._wait_for_cart_count_increment(previous_count, timeout=5)
            except Exception:
                self.log_warn("Cart badge did not increment in time; continuing with total verification.")
        expected_total = sum(selected_prices)

        # Open cart
        self.click(self.CART_ICON)

        # Wait for cart total to settle before reading value.
        self.log_step("Waiting for cart total recalculation")
        self._wait(
            lambda d: d.find_element(*self.CART_TOTAL_PRICE).text.strip().startswith("$"),
            timeout=8,
        )

        try:
            # Read total value element
            total_element = self.driver.find_element(*self.CART_TOTAL_PRICE)
            actual_total_text = total_element.text
            self.log_info(f"Raw cart total text: '{actual_total_text}'")

            # Convert "$1,234.56" -> 1234.56
            actual_total = float(actual_total_text.replace('$', '').replace(',', '').strip())
        except Exception as e:
            # Preserve context if total cannot be parsed.
            self.log_error(f"Failed to read cart total: {e}")
            raise

        cart_line_prices = self.get_cart_line_item_prices()
        cart_line_total = sum(cart_line_prices)

        self.log_assert(f"Expected total: ${expected_total:.2f}")
        self.log_assert(f"Actual total: ${actual_total:.2f}")
        self.log_assert(f"Cart line-items sum: ${cart_line_total:.2f}")

        assert round(cart_line_total, 2) == round(actual_total, 2), (
            f"CART LINE SUM ERROR: line-items total {cart_line_total} does not match subtotal {actual_total}"
        )

        # Use round() to avoid float precision artifacts.
        assert round(actual_total, 2) == round(expected_total, 2), \
            f"TOTAL ERROR: got {actual_total}, expected {expected_total}"
        self.log_done("Cart total is correct")

    def _current_cart_count(self):
        """Return current numeric cart badge value; fallback to 0 when badge is missing."""
        badge_candidates = self.driver.find_elements(By.CSS_SELECTOR, ".k-badge, .cart-count")
        for badge in badge_candidates:
            text = badge.text.strip()
            if text.isdigit():
                return int(text)
        return 0

    def _wait_for_cart_count_increment(self, previous_count, timeout=2):
        self._wait(lambda d: self._current_cart_count() > previous_count, timeout=timeout)

    def _get_remove_buttons(self):
        """Return visible remove controls from supported cart templates."""
        fallback_locators = [
            self.REMOVE_ITEM_BUTTONS,
            (By.XPATH, "//p[normalize-space()='Remove']"),
            (By.XPATH, "//button[contains(@class, 'remove-product') or normalize-space()='Remove']"),
        ]
        for locator in fallback_locators:
            elements = self.driver.find_elements(*locator)
            visible_elements = []
            for element in elements:
                try:
                    if element.is_displayed():
                        visible_elements.append(element)
                except Exception:
                    # Element can become stale during cart re-render; ignore and keep searching.
                    continue
            if visible_elements:
                return visible_elements
        return []

    def _is_cart_empty_visible(self):
        return len(self.driver.find_elements(*self.EMPTY_CART_MESSAGE)) > 0

    def clear_cart(self):
        """Stable cart clearing by force-navigating after cleanup."""
        self.log_step("Błyskawiczne czyszczenie koszyka...")

        # Clear session
        script = "localStorage.clear(); sessionStorage.clear();"
        self.driver.execute_script(script)

        # INSTEAD of refresh(), use your open method to go back to the source
        self.driver.get(self.BIKE_MAIN_LINK)

        # Wait for a 'stabilizer' element (like the category titles)
        self.wait_for_all_visible(self.BIKE_CATEGORY_TITLES, timeout=10)



    """Navigation methods."""

    def open_bikes_main_link(self):
        """Open bikes landing page."""
        self.open(self.BIKE_MAIN_LINK)
        self._wait_for_bikes_landing_ready(timeout=5)

    def open_mountain_bikes(self):
        """Open Mountain Bikes category."""
        self.click(self.MOUNTAINS_BIKES_CATEGORY)
        self._wait_for_product_grid_ready(timeout=5)

    def _wait_for_bikes_landing_ready(self, timeout=5):
        """Wait for bikes landing page regardless of whether pager is visible yet."""
        self.wait_for_url("Home/Bikes", timeout=timeout)
        self._wait(
            lambda d: len(d.find_elements(*self.BIKE_CATEGORY_TITLES)) > 0
            or len(d.find_elements(*self.PRODUCT_CARD)) > 0
            or len(d.find_elements(*self.PAGER_INFO)) > 0,
            timeout=timeout,
        )

    def _wait_for_product_grid_ready(self, timeout=5):
        """Wait for product cards and related listing markers to appear."""
        self._wait(
            lambda d: len(d.find_elements(*self.PRODUCT_CARD)) > 0
            and (
                len(d.find_elements(*self.PAGER_INFO)) > 0
                or len(d.find_elements(*self.DISCOUNT_PERCENT_BADGE)) >= 0
            ),
            timeout=timeout,
        )

    """Data getters."""

    def get_all_prices(self):
        """Collect all product prices and convert to float."""
        PRICE_LOCATOR = (By.XPATH, "//div[@class='card-price']")
        elements = self.driver.find_elements(*PRICE_LOCATOR)
        prices = []
        for el in elements:
            clean_text = el.text.replace('$', '').replace(',', '').strip()
            if clean_text:
                prices.append(float(clean_text))
        return prices

    def get_all_names(self):
        """Collect all product names."""
        NAME_LOCATOR = (By.XPATH, "//div[@class='k-card-title']")
        elements = self.driver.find_elements(*NAME_LOCATOR)
        return [el.text.strip() for el in elements if el.text]

    def get_all_discount_labels(self):
        """Collect discount badge labels (e.g., '20% off')."""
        elements = self.driver.find_elements(*self.DISCOUNT_PERCENT_BADGE)
        return [el.text.strip() for el in elements if el.text]

    @staticmethod
    def _parse_price_text(text):
        match = re.search(r"([0-9]+(?:,[0-9]{3})*(?:\.[0-9]{2})?)", text.replace("$", ""))
        if not match:
            raise ValueError(f"Could not parse price from text: '{text}'")
        return float(match.group(1).replace(",", ""))

    def get_cart_line_item_prices(self):
        self.log_info("[POM] Pobieram ceny produktów z koszyka...")

        # Używamy wait_for_all_visible, bo find_elements nie czeka i często zwraca [] przy asynchronicznym UI
        try:
            # Zakładam, że CART_LINE_ITEM_PRICES to ten poprawiony, prostszy lokator
            price_elements = self.wait_for_all_visible(self.CART_LINE_ITEM_PRICES, timeout=7)
        except Exception as e:
            self.log_warn(f"[POM] Timeout przy czekaniu na ceny: {e}. Próbuję pobrać co jest dostępne...")
            price_elements = self.driver.find_elements(*self.CART_LINE_ITEM_PRICES)

        prices = []
        for element in price_elements:
            try:
                # Pobieramy tekst tylko od widocznych elementów
                if element.is_displayed():
                    text = element.text.strip()
                    if text:
                        prices.append(self._parse_price_text(text))
            except Exception as e:
                self.log_warn(f"[POM] Błąd przy parsowaniu ceny pojedynczego elementu: {e}")
                continue

        if not prices:
            # Screenshot w Allure to złoto przy debugowaniu
            allure.attach(
                self.driver.get_screenshot_as_png(),
                name="failed_cart_prices_view",
                attachment_type=allure.attachment_type.PNG
            )
            # Logujemy HTML, żebyś widział w raporcie, co Selenium faktycznie "widziało" w DOMie
            allure.attach(self.driver.page_source, name="page_source", attachment_type=allure.attachment_type.TEXT)
            raise AssertionError("Nie znaleziono żadnych cen produktów w koszyku!")

        self.log_info(f"[POM] Odczytano {len(prices)} cen: {prices}")
        return prices

    def get_total_count_from_pager(self):
        """Extract total item count from pager text."""
        text_info = self.driver.find_element(*self.PAGER_INFO).text
        # Split example: ['1', '-', '12', 'of', '32', 'items'] -> index 4
        parts = text_info.split()
        return int(parts[4])

    def get_bike_category_titles(self):
        """Collect text for bike category headers."""
        elements = self.wait_for_all_visible(self.BIKE_CATEGORY_TITLES)
        return [el.text.strip() for el in elements]

    def assert_expected_bike_categories(self, expected_titles=None):
        titles = self.get_bike_category_titles()
        self.log_info(f"Bike categories found: {titles}")
        expected = expected_titles or ["Mountain Bikes", "Road Bikes", "Touring Bikes"]
        for expected_title in expected:
            assert expected_title in titles, f"Expected category '{expected_title}' in {titles}"

    """Counter helpers."""

    def count_visible_bikes(self):
        """Count cards with non-empty visible title text."""
        # Read title elements inside cards.
        titles = self.driver.find_elements(By.XPATH, "//div[contains(@class, 'k-card')]//div[@class='k-card-title']")

        # Count only entries with non-empty text.
        visible_titles = [t for t in titles if t.text.strip() != ""]

        return len(visible_titles)

    def count_badges(self):
        """Count discount percentage badges visible on screen."""
        return len(self.get_all_discount_labels())

    """Validation helpers."""

    def verify_discount_filter(self):
        """Validate discounted filter consistency."""
        self.log_step("Applying discounted-items filter")
        self.click(self.DISCOUNTED_BIKES_FILTER)
        self._wait_for_product_grid_ready(timeout=6)

        bikes_count = self.count_visible_bikes()
        badges_count = self.count_badges()

        self.log_info(f"Discount filter debug: products={bikes_count}, badges={badges_count}")

        assert bikes_count > 0, "ERROR: Discount filter returned no results."
        assert bikes_count == badges_count, (
            f"FILTER ERROR: displayed {bikes_count} products, "
            f"but only {badges_count} has a discount badge."
        )
        self.log_done("All visible products have discount badges")

    def all_sorting_options(self):
        """Validate all sorting options one-by-one."""
        scenarios = [
            (self.SORT_FILTER_A_TO_Z, "name_asc"),
            (self.SORT_FILTER_Z_TO_A, "name_desc"),
            (self.SORT_FILTER_LOW_TO_HIGH, "price_asc"),
            (self.SORT_FILTER_HIGH_TO_LOW, "price_desc")
        ]

        for locator, sort_type in scenarios:
            self.click(self.SORT_DROPDOWN_TRIGGER)
            try:
                option_element = self.wait_for_visible(locator, timeout=4)
            except TimeoutException:
                # Kendo dropdown can collapse right after opening; reopen and use presence fallback.
                self.click_with_js(self.SORT_DROPDOWN_TRIGGER)
                option_element = self.wait_for_presence(locator, timeout=4)

            option_name = option_element.text
            try:
                self.safe_click(locator, retries=2)
            except TimeoutException:
                self.log_warn(f"Standard sort-option click failed; using JS click for '{option_name}'")
                self.driver.execute_script("arguments[0].click();", option_element)

            self._wait(
                lambda d: option_name.lower() in d.find_element(*self.SORT_DROPDOWN_TRIGGER).text.lower(),
                timeout=5,
            )

            if "Price" in option_name:
                actual = self.get_all_prices()
                is_desc = (sort_type == "price_desc")
                assert actual == sorted(actual, reverse=is_desc), f"Price sorting error: {option_name}"
            elif "Name" in option_name:
                actual = self.get_all_names()
                is_desc = (sort_type == "name_desc")
                assert actual == sorted(actual, reverse=is_desc), f"Name sorting error: {option_name}"

            self.log_done(f"Sorting '{option_name}' works correctly")

    def assert_products_available_for_all_filter(self):
        self.click(self.ALL_BIKES_FILTER)
        self._wait_for_product_grid_ready(timeout=5)
        all_items_count = self.get_total_count_from_pager()
        assert all_items_count > 0, f"Expected all-items count > 0, got {all_items_count}"
        return all_items_count

    def assert_discounted_filter_consistency(self, expected_all_count=None):
        self.click(self.DISCOUNTED_BIKES_FILTER)
        self._wait_for_product_grid_ready(timeout=5)
        discounted_pager_count = self.get_total_count_from_pager()
        discounted_badges_count = self.count_badges()
        discounted_cards_count = self.count_visible_bikes()
        if expected_all_count is not None:
            assert discounted_pager_count <= expected_all_count, (
                f"Expected discounted count ({discounted_pager_count}) <= all items ({expected_all_count})"
            )
        assert discounted_pager_count > 0, (
            f"Expected discounted pager count > 0, got {discounted_pager_count}"
        )
        assert discounted_badges_count == discounted_pager_count, (
            f"Expected discounted badges ({discounted_badges_count}) to match pager ({discounted_pager_count})"
        )
        assert discounted_cards_count == discounted_pager_count, (
            f"Expected discounted cards ({discounted_cards_count}) to match pager ({discounted_pager_count})"
        )

    def assert_filter_counts_consistent(self):
        all_items_count = self.assert_products_available_for_all_filter()
        self.assert_discounted_filter_consistency(expected_all_count=all_items_count)