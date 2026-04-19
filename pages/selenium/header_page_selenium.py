from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    StaleElementReferenceException,
    TimeoutException,
)
from pages.selenium.base_page_selenium import BasePage


class HeaderPage(BasePage):
    # --- LOCATORS ---
    SHOPPING_CART_BTN = (By.XPATH, "//a[contains(@href, 'ShoppingCart')]")
    CATEGORIES_MENU = (By.XPATH, "//span[normalize-space()='Categories']")

    # Category locators
    ACCESSORIES_LINK = (By.XPATH, "//a[contains(@class, 'k-menu-link') and normalize-space()='Accessories']")
    BIKES_LINK = (By.XPATH, "//a[contains(@class, 'k-menu-link') and normalize-space()='Bikes']")
    CLOTHES_LINK = (By.XPATH, "//a[contains(@class, 'k-menu-link') and normalize-space()='Clothes']")
    COMPONENTS_LINK = (By.XPATH, "//a[contains(@class, 'k-menu-link') and normalize-space()='Components']")

    # --- BASIC METHODS ---

    def click_cart(self):
        self.click(self.SHOPPING_CART_BTN)

    def open_home_page(self):
        """Navigate user to the e-shop home page."""
        self.open("https://demos.telerik.com/kendo-ui/eshop")

    def get_url(self):
        return self.driver.current_url

    def assert_url_contains(self, expected_fragment):
        self.wait_for_url(expected_fragment, timeout=10)
        current_url = self.get_url()
        assert expected_fragment in current_url, (
            f"Expected URL containing '{expected_fragment}', got '{current_url}'"
        )

    def validate_header_navigation(self):
        checks = [
            ("ShoppingCart", self.click_cart),
            ("eshop", self.open_home_page),
            ("Home/Accessories", self.open_accessories_category),
            ("Home/Bikes", self.open_bikes_category),
            ("Home/Clothing", self.open_clothes_category),
            ("Home/Components", self.open_components_category),
        ]

        for expected_fragment, action in checks:
            self.open_home_page()
            action()
            self.assert_url_contains(expected_fragment)




    # --- CATEGORY METHODS ---

    def open_accessories_category(self):
        self._hover_and_click(self.ACCESSORIES_LINK)

    def open_bikes_category(self):
        self._hover_and_click(self.BIKES_LINK)

    def open_clothes_category(self):
        self._hover_and_click(self.CLOTHES_LINK)

    def open_components_category(self):
        self._hover_and_click(self.COMPONENTS_LINK)

    # Shared hover-and-click logic
    def _hover_and_click(self, locator):
        categories = self.wait_for_visible(self.CATEGORIES_MENU, timeout=8)
        # Scroll to menu so it is visible and interactable.
        self.driver.execute_script("arguments[0].scrollIntoView(true);", categories)

        actions = ActionChains(self.driver)
        actions.move_to_element(categories).pause(0.25).perform()

        try:
            self.wait_for_clickable(locator, timeout=8).click()
        except (TimeoutException, StaleElementReferenceException, ElementClickInterceptedException):
            # Fallback to JS click for transient overlay/menu timing issues.
            print(f"Standard click failed; using JS click for: {locator}")
            element = self.wait_for_visible(locator, timeout=6)
            self.driver.execute_script("arguments[0].click();", element)


