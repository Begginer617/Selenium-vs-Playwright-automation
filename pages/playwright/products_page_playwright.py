from playwright.sync_api import expect
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
        self.log_step(f"Navigating to bikes landing page: {self.BIKE_MAIN_LINK}")
        self.page.goto(self.BIKE_MAIN_LINK)
        return self

    def get_bike_category_titles_pw(self):
        self.log_step("Collecting bike category titles")
        return self.page.locator(self.BIKE_CATEGORY_TITLES).all_inner_texts()

    def open_mountain_bikes_pw(self):
        self.log_step("Opening category: Mountain Bikes")
        self.page.locator(self.MOUNTAIN_BIKES).first.click()
        self.page.wait_for_load_state("networkidle")
        return self

    def click_filter_all_pw(self):
        self.log_step("Applying filter: All")
        self.page.locator(self.ALL_BIKES_FILTER).click()
        self.page.wait_for_timeout(1000)
        return self

    def click_filter_discounted_pw(self):
        self.log_step("Applying filter: Discounted items only")
        self.page.locator(self.DISCOUNTED_BIKES_FILTER).click()
        self.page.wait_for_timeout(1000)
        return self

    def get_total_count_from_pager_pw(self):
        self.log_step("Reading product count from pager")
        self.page.wait_for_selector(self.PAGER_INFO, state="visible", timeout=5000)
        text = self.page.locator(self.PAGER_INFO).inner_text()
        self.log_info(f"Pager text: '{text}'")
        count = int(text.split("of")[-1].strip().split(" ")[0])
        self.log_info(f"Parsed pager count: {count}")
        return count

    def assert_expected_bike_categories_pw(self, expected_titles=None):
        titles = self.get_bike_category_titles_pw()
        self.log_info(f"Bike categories found: {titles}")
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
        self.log_info(f"Discount badge count: {count}")
        return count

    def debug_page_content_pw(self):
        all_badges = self.page.locator("//span[contains(@class, 'k-badge')]").all_inner_texts()
        self.log_info(f"Badges visible on page: {all_badges}")

    def count_visible_bikes_pw(self):
        count = self.page.locator(self.PRODUCT_CARDS).filter(has=self.page.locator(".discount-pct")).count()
        self.log_info(f"Visible discounted cards count: {count}")
        return count

    def clear_cart_pw(self):
        self.log_step("Starting cart cleanup")
        self.go_to_cart_pw()
        self.page.on("dialog", lambda dialog: dialog.accept())
        while self.page.locator(f"xpath={self.REMOVE_BTN}").count() > 0:
            self.log_step("Removing cart item")
            self.page.locator(f"xpath={self.REMOVE_BTN}").first.click()
        self.log_done("Cart is empty")
        return self


    def go_to_cart_pw(self):
        self.log_step("Opening shopping cart")
        self.page.click(f"xpath={self.CART_ICON}")
        return self

    def add_first_product_pw(self):
        self.log_step("Adding first product to cart")
        # Use .first to explicitly target the first matching element.
        self.page.locator(f"xpath={self.ADD_TO_CART_BTN}").first.click()
        return self

    def get_all_prices_pw(self):
        self.log_step("Collecting product prices")
        locators = self.page.locator(f"xpath={self.PRICE_LABELS}")
        return [float(el.inner_text().replace('$', '').replace(',', '')) for el in locators.all()]

    def get_all_names_pw(self):
        self.log_step("Collecting product names")
        locators = self.page.locator(f"xpath={self.PRODUCT_TITLES}")
        return [el.inner_text().strip() for el in locators.all()]

    def add_first_product_to_cart_and_verify_pw(self):
        product_names = self.get_all_names_pw()
        first_product_name = product_names[0]
        self.log_info(f"Selected product: '{first_product_name}'")

        self.log_step("Adding selected product to cart")
        self.add_first_product_pw()

        self.log_step("Opening cart for verification")
        self.go_to_cart_pw()

        self.log_assert(f"Checking whether '{first_product_name}' is visible in cart")
        cart_item_locator = self.page.locator(f"//*[contains(text(), '{first_product_name}')]")

        expect(cart_item_locator.first).to_be_visible()
        self.log_done("Product element found in cart")

        expect(cart_item_locator.first).to_contain_text(first_product_name)
        self.log_done("Cart item name matches selected product")
        return self

    def all_sorting_options_pw(self):
        self.log_step("Starting sorting sequence")

        # Open sorting dropdown.
        self.page.locator(self.SORT_TRIGGER).click()

        # Choose option: Price - High to Low.
        self.page.locator("li[role='option']:has-text('Price - High to Low')").click()

        self.log_step("Applied sort: Price - High to Low")
        self.page.wait_for_timeout(1000)

        # Open dropdown again.
        self.page.locator(self.SORT_TRIGGER).click()

        # Choose option: Price - Low to High.
        self.page.locator("li[role='option']:has-text('Price - Low to High')").click()

        self.log_step("Applied sort: Price - Low to High")
        self.page.wait_for_timeout(1000)

        self.log_done("Sorting sequence finished")

    def add_multiple_products_and_verify_total_pw(self, count=5):
        self.log_step(f"Starting total-price validation for {count} products")

        # Collect all visible prices from product cards.
        all_prices = self.get_all_prices_pw()

        if len(all_prices) < count:
            raise Exception(
                f"Found only {len(all_prices)} products on page, but {count} are required."
            )

        # Calculate expected subtotal based on selected products.
        selected_prices = all_prices[:count]
        expected_total = sum(selected_prices)
        self.log_info(f"Selected prices: {selected_prices}, expected total: ${expected_total:.2f}")

        # Add selected products to cart.
        add_buttons = self.page.locator(f"xpath={self.ADD_TO_CART_BTN}")

        for i in range(count):
            self.log_step(f"Adding product {i + 1}/{count}")
            add_buttons.nth(i).click()
            self.page.wait_for_timeout(200)  # Small delay for cart update animation.

        # Navigate to cart.
        self.go_to_cart_pw()

        # Verify subtotal value in cart.
        total_element = self.page.locator(f"#{self.CART_TOTAL_PRICE}")
        expect(total_element).to_be_visible()

        actual_total = float(total_element.inner_text().replace('$', '').replace(',', '').strip())

        self.log_assert(f"Cart total is ${actual_total:.2f}")
        assert round(actual_total, 2) == round(expected_total, 2)
        self.log_done("Cart total matches expected value")
