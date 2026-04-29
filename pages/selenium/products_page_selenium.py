import contextlib
import re
import time

import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    ElementNotInteractableException,
    StaleElementReferenceException,
    TimeoutException,
    UnexpectedAlertPresentException,
)
from selenium.webdriver.support.wait import WebDriverWait

from pages.selenium.base_page_selenium import BasePage


class ProductsPage(BasePage):
    """Constants and links."""
    BIKE_MAIN_LINK = "https://demos.telerik.com/kendo-ui/eshop/Home/Bikes"
    SHOPPING_CART_URL = "https://demos.telerik.com/kendo-ui/eshop/Account/ShoppingCart"

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
        try:
            self._wait_for_cart_count_increment(previous_count, timeout=4)
        except TimeoutException:
            # Badge can lag on slow networks; cart assertion below still validates outcome.
            self.log_warn("Cart badge did not increment before opening cart; continuing.")

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

    def _product_cards_with_add_to_cart(self):
        """Product cards that contain an add-to-cart control (order matches the grid)."""
        cards = self.driver.find_elements(*self.PRODUCT_CARD)
        with_cart = []
        for card in cards:
            try:
                if card.find_elements(By.CLASS_NAME, "add-to-cart"):
                    with_cart.append(card)
            except Exception:
                continue
        return with_cart

    def add_multiple_products_and_verify_total(self, count=5):
        """Add N products and verify total cart value."""
        self.log_step(f"Starting cart total validation for {count} products")
        selected_prices = []

        # Add products
        for i in range(count):
            # Price and button from the same card — avoids mismatch between get_all_prices() and all .add-to-cart.
            self._wait_for_product_grid_ready(timeout=8)
            cards = self._product_cards_with_add_to_cart()
            if i >= len(cards):
                raise AssertionError(
                    f"Could not find product card with add-to-cart for index {i}. "
                    f"Only {len(cards)} cards found."
                )
            card = cards[i]
            price_el = card.find_element(By.CSS_SELECTOR, ".card-price")
            clean_text = price_el.text.replace("$", "").replace(",", "").strip()
            if not clean_text:
                raise AssertionError(f"Empty price on product card at index {i}.")
            price_value = float(clean_text)
            selected_prices.append(price_value)
            self.log_step(f"Adding product #{i + 1} priced at ${price_value}")
            add_btn = card.find_element(By.CLASS_NAME, "add-to-cart")
            previous_count = self._current_cart_count()
            add_btn.click()
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
            lambda d: "$" in d.find_element(*self.CART_TOTAL_PRICE).text.strip(),
            timeout=8,
        )

        try:
            # Read total value element
            total_element = self.driver.find_element(*self.CART_TOTAL_PRICE)
            actual_total_text = total_element.text
            self.log_info(f"Raw cart total text: '{actual_total_text}'")

            # Convert "$1,234.56" or "$ 1,234.56" -> 1234.56
            normalized = re.sub(r"\s+", "", actual_total_text.replace("$", "").replace(",", ""))
            actual_total = float(normalized)
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
        """Return current numeric cart header badge; avoid list-page discount .k-badge (e.g. 20% -> 20)."""
        for locator in (
            (By.ID, "shopping-cart-badge"),
            (By.CSS_SELECTOR, "a[href*='Cart'] .k-badge, a[href*='ShoppingCart'] .k-badge, .cart-count"),
        ):
            for badge in self.driver.find_elements(*locator):
                try:
                    text = badge.text.strip()
                    if text.isdigit():
                        return int(text)
                except Exception:
                    continue
        return 0

    def _wait_for_cart_count_increment(self, previous_count, timeout=2):
        self._wait(lambda d: self._current_cart_count() > previous_count, timeout=timeout)

    def _get_remove_buttons(self):
        """Return visible remove controls from supported cart templates."""
        fallback_locators = [
            self.REMOVE_ITEM_BUTTONS,
            (By.XPATH, "//p[normalize-space()='Remove']"),
            (By.XPATH, "//button[contains(@class, 'remove-product') or normalize-space()='Remove']"),
            # Telerik eShop: shopping_cart.js uses id="remove_<itemId>" on a control in the Kendo grid
            (By.CSS_SELECTOR, "[id^='remove_']"),
            (By.XPATH, "//*[@id[starts-with(.,'remove_')]]"),
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

    def _is_cart_empty_message_visible(self):
        """DOM message such as 'Your shopping cart is empty'."""
        self._accept_any_alert()
        if self.driver.find_elements(*self.EMPTY_CART_MESSAGE):
            return True
        # Alternate copy on some builds / locales
        alt = (
            By.XPATH,
            "//*[contains(translate(normalize-space(.), "
            "'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), "
            "'nothing in your cart') or contains(translate(normalize-space(.), "
            "'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'shopping cart is empty')]",
        )
        return len(self.driver.find_elements(*alt)) > 0

    def _cart_kendo_item_count(self):
        """Approximate line-item count from Kendo grid when present; -1 if unavailable."""
        self._accept_any_alert()
        with contextlib.suppress(Exception):
            n = self.driver.execute_script(
                """
                if (!window.jQuery) { return -1; }
                var g = jQuery("#shoppingCartGrid").data("kendoGrid");
                if (!g) { return -1; }
                try {
                    var ds = g.dataSource;
                    if (ds && typeof ds.total === "function") { return ds.total(); }
                    return g.items().length;
                } catch (e) { return -1; }
                """
            )
            if n is not None:
                return int(n)
        return -1

    def _is_cart_effectively_empty(self):
        """True when cart page shows no line items (message and/or zero Kendo rows)."""
        if self._is_cart_empty_message_visible():
            return True
        n = self._cart_kendo_item_count()
        if n == 0:
            return True
        return False

    def assert_shopping_cart_empty(self, timeout=12):
        """
        Open the cart page and fail fast if line items or totals still indicate a non-empty cart.
        Call after clear_cart() when the test depends on a zero baseline.
        On success, navigates to Home/Bikes (same as clear_cart()) so the next step can open categories.
        """
        self._get_url_fast(
            self.SHOPPING_CART_URL,
            "ShoppingCart",
            part_timeout=max(12, timeout),
        )
        try:
            self._wait(lambda d: self._is_cart_effectively_empty(), timeout=timeout)
        except TimeoutException as exc:
            n = self._cart_kendo_item_count()
            badge = self._current_cart_count()
            raise AssertionError(
                f"Shopping cart is not empty (kendo_items={n}, header_badge_count={badge})."
            ) from exc
        # Match clear_cart() post-condition: listing tests expect Home/Bikes context.
        self._open_bikes_landing_from_clear()

    def _clear_cart_via_remove_buttons(self, max_clicks=40):
        """Remove line items via visible Remove controls (real UI / server sync)."""
        for _ in range(max_clicks):
            if self._is_cart_effectively_empty():
                return True
            buttons = self._get_remove_buttons()
            if not buttons:
                break
            btn = buttons[0]
            try:
                self.driver.execute_script(
                    "arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});", btn
                )
            except Exception:
                pass
            try:
                btn.click()
            except (StaleElementReferenceException, ElementNotInteractableException):
                with contextlib.suppress(Exception):
                    self.driver.execute_script("arguments[0].click();", btn)
            self._accept_any_alert()
            try:
                self._wait(
                    lambda d: self._is_cart_effectively_empty()
                    or len(self._get_remove_buttons()) < len(buttons),
                    timeout=5,
                )
            except (TimeoutException, UnexpectedAlertPresentException):
                self._accept_any_alert()
                self.log_warn("Remove click did not update cart DOM in time; retrying.")
        return self._is_cart_effectively_empty()

    def _get_page_load_timeout(self):
        t = 4.0
        with contextlib.suppress(Exception):
            timeouts = getattr(self.driver, "timeouts", None)
            if timeouts is not None and getattr(timeouts, "page_load", None) is not None:
                t = float(timeouts.page_load)
        return t

    def _set_page_load_timeout(self, seconds):
        with contextlib.suppress(Exception):
            self.driver.set_page_load_timeout(seconds)

    def _accept_any_alert(self):
        with contextlib.suppress(Exception):
            self.driver.switch_to.alert.accept()

    def _get_url_fast(self, url, url_part, part_timeout=8):
        """One navigation with a bounded page-load timeout; avoids long BasePage.open() retries."""
        self._accept_any_alert()
        old = self._get_page_load_timeout()
        with contextlib.suppress(Exception):
            self._set_page_load_timeout(max(10, part_timeout + 2))
        try:
            with contextlib.suppress(Exception):
                self.driver.get(url)
        except Exception:
            # Brief explicit wait for navigation to settle instead of a blind sleep.
            with contextlib.suppress(TimeoutException):
                self.wait_for_url(url_part, timeout=2)
        with contextlib.suppress(TimeoutException):
            self.wait_for_url(url_part, timeout=part_timeout)
        with contextlib.suppress(Exception):
            self._set_page_load_timeout(old)

    def _open_bikes_landing_from_clear(self):
        self._get_url_fast(self.BIKE_MAIN_LINK, "Home/Bikes", part_timeout=10)
        self._wait_for_bikes_landing_ready(timeout=8)

    def _clear_shopping_cart_grid_kendo(self):
        """
        Pop all Kendo grid rows and sync to the server (Telerik eShop /js/shopping_cart.js).
        """
        with contextlib.suppress(Exception):
            return int(
                self.driver.execute_script(
                    r"""
            if (!window.jQuery) { return 0; }
            var oldc = window.confirm, n = 0;
            try {
                window.confirm = function() { return true; };
                var g = jQuery("#shoppingCartGrid").data("kendoGrid");
                if (!g) { return 0; }
                var guard = 300;
                while (guard-- > 0) {
                    var rows = g.tbody ? g.tbody.find("tr") : jQuery();
                    if (!rows || !rows.length) { break; }
                    g.removeRow(jQuery(rows[0]));
                    n++;
                    g.dataSource.sync();
                }
            } finally {
                window.confirm = oldc;
            }
            if (typeof calculateShoppingCartTotal === "function") { try { calculateShoppingCartTotal(); } catch (e) {} }
            if (typeof getShoppingCartItemsCount === "function") { try { getShoppingCartItemsCount(); } catch (e) {} }
            return n;
                    """
                )
                or 0
            )
        return 0

    def clear_cart(self):
        """
        Empty the in-app shopping cart (server state), then return to the bikes page.

        Prefer the same path as a user: visible Remove controls (locators), then optional
        Kendo bulk clear if rows remain. Raises if the cart cannot be emptied.
        """
        self.log_step("Clearing shopping cart...")

        with contextlib.suppress(Exception):
            self.driver.execute_script("localStorage.clear(); sessionStorage.clear();")

        for attempt in range(4):
            self._get_url_fast(
                self.SHOPPING_CART_URL,
                "ShoppingCart",
                part_timeout=12,
            )
            try:
                self._wait(
                    lambda d: self._is_cart_effectively_empty()
                    or len(d.find_elements(By.ID, "shoppingCartGrid")) > 0
                    or len(d.find_elements(*self.REMOVE_ITEM_BUTTONS)) > 0
                    or len(d.find_elements(By.CSS_SELECTOR, "[id^='remove_']")) > 0,
                    timeout=10,
                )
            except TimeoutException:
                self.log_warn("Cart page shell did not stabilize in time; attempting clear anyway.")

            if self._is_cart_effectively_empty():
                self._open_bikes_landing_from_clear()
                return

            # 1) Locator-driven removes first (stable, mirrors manual testing).
            self._clear_cart_via_remove_buttons()
            try:
                self._wait(lambda d: self._is_cart_effectively_empty(), timeout=12)
            except TimeoutException:
                self.log_warn(
                    f"Cart still has items after Remove-locator pass (attempt {attempt + 1}/4)."
                )

            if self._is_cart_effectively_empty():
                self._open_bikes_landing_from_clear()
                return

            # 2) Bulk Kendo clear, then Remove again for anything left.
            self._clear_shopping_cart_grid_kendo()
            self._clear_cart_via_remove_buttons()
            try:
                self._wait(lambda d: self._is_cart_effectively_empty(), timeout=12)
            except TimeoutException:
                self.log_warn(
                    f"Cart still not empty after Kendo + Remove pass (attempt {attempt + 1}/4)."
                )

            if self._is_cart_effectively_empty():
                self._open_bikes_landing_from_clear()
                return

        self._get_url_fast(
            self.SHOPPING_CART_URL,
            "ShoppingCart",
            part_timeout=12,
        )
        if not self._is_cart_effectively_empty():
            raise AssertionError(
                "clear_cart() could not empty the shopping cart: "
                "Remove locators and Kendo grid clear were insufficient. "
                "See assert_shopping_cart_empty() for a hard check in tests."
            )
        self._open_bikes_landing_from_clear()



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
        # `len(...) >= 0` was always true, so the wait effectively required only cards
        # and could return before pager/Kendo finished rendering (flaky clicks/asserts).
        self._wait(
            lambda d: len(d.find_elements(*self.PRODUCT_CARD)) > 0
            and (
                len(d.find_elements(*self.PAGER_INFO)) > 0
                or len(d.find_elements(*self.DISCOUNT_PERCENT_BADGE)) > 0
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
        self.log_info("[POM] Reading product line prices from the cart...")

        # Use wait_for_all_visible because find_elements does not wait and often returns [] for async UI
        try:
            # CART_LINE_ITEM_PRICES is the shared locator for cart line prices
            price_elements = self.wait_for_all_visible(self.CART_LINE_ITEM_PRICES, timeout=7)
        except Exception as e:
            self.log_warn(f"[POM] Timed out waiting for cart line prices: {e}. Falling back to find_elements.")
            price_elements = self.driver.find_elements(*self.CART_LINE_ITEM_PRICES)

        prices = []
        for element in price_elements:
            try:
                # Use visible elements only
                if element.is_displayed():
                    text = element.text.strip()
                    if text:
                        prices.append(self._parse_price_text(text))
            except Exception as e:
                self.log_warn(f"[POM] Error parsing a single line price: {e}")
                continue

        if not prices:
            # Screenshot in Allure helps when debugging
            allure.attach(
                self.driver.get_screenshot_as_png(),
                name="failed_cart_prices_view",
                attachment_type=allure.attachment_type.PNG
            )
            # Attach HTML so reports show what the DOM actually contained
            allure.attach(self.driver.page_source, name="page_source", attachment_type=allure.attachment_type.TEXT)
            raise AssertionError("No product prices found in the cart.")

        self.log_info(f"[POM] Read {len(prices)} prices: {prices}")
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
                self.safe_click(locator, retries=3)
            except TimeoutException:
                self.log_warn(f"Standard sort-option click failed; using JS click for '{option_name}'")
                try:
                    fresh = self.wait_for_visible(locator, timeout=3)
                    self.driver.execute_script("arguments[0].click();", fresh)
                except (TimeoutException, StaleElementReferenceException):
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