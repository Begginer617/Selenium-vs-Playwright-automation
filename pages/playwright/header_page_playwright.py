from playwright.sync_api import Page, expect

class HeaderPagePw:
    def __init__(self, page: Page):
        self.page = page
        # Reuse the same locators as Selenium for fair framework comparison.
        self.SHOPPING_CART_BTN = "//a[contains(@href, 'ShoppingCart')]"
        self.CATEGORIES_MENU = "//span[normalize-space()='Categories']"
        self.ACCESSORIES_LINK = "//a[contains(@class, 'k-menu-link') and normalize-space()='Accessories']"
        self.BIKES_LINK = "//a[contains(@class, 'k-menu-link') and normalize-space()='Bikes']"
        self.CLOTHES_LINK = "//a[contains(@class, 'k-menu-link') and normalize-space()='Clothes']"
        self.COMPONENTS_LINK = "//a[contains(@class, 'k-menu-link') and normalize-space()='Components']"

    def click_cart_pw(self):
        self.page.locator(self.SHOPPING_CART_BTN).first.click()

    def open_home_page_pw(self):
        self.page.goto("https://demos.telerik.com/kendo-ui/eshop", wait_until="domcontentloaded")

    def get_url_pw(self):
        return self.page.url

    def assert_url_contains_pw(self, expected_fragment: str):
        expect(self.page).to_have_url(f"**{expected_fragment}**")

    def validate_header_navigation_pw(self):
        checks = [
            ("ShoppingCart", self.click_cart_pw),
            ("eshop", self.open_home_page_pw),
            ("Home/Accessories", self.open_accessories_category_pw),
            ("Home/Bikes", self.open_bikes_category_pw),
            ("Home/Clothing", self.open_clothes_category_pw),
            ("Home/Components", self.open_components_category_pw),
        ]

        for expected_fragment, action in checks:
            self.open_home_page_pw()
            action()
            self.assert_url_contains_pw(expected_fragment)

    # Category hover helper methods
    def _hover_menu_pw(self):
        # Select first matching element to avoid strict-mode ambiguity.
        self.page.locator(self.CATEGORIES_MENU).first.hover()

    def open_accessories_category_pw(self):
        self._hover_menu_pw()
        self.page.locator(self.ACCESSORIES_LINK).click()

    def open_bikes_category_pw(self):
        self._hover_menu_pw()
        self.page.locator(self.BIKES_LINK).click()

    def open_clothes_category_pw(self):
        self._hover_menu_pw()
        self.page.locator(self.CLOTHES_LINK).click()

    def open_components_category_pw(self):
        self._hover_menu_pw()
        self.page.locator(self.COMPONENTS_LINK).click()