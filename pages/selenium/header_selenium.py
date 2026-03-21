from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from pages.selenium.base_page_selenium import BasePage

class HeaderSelenium(BasePage):
    # 1. Definiujemy SAME ADRESY (Lokatory). To są krotki (tuples).
    SHOPPING_CART_BTN = (By.XPATH, "//a[contains(@href, 'ShoppingCart')]")
    SHOPPING_CART_COUNT = (By.ID, "shopping-cart-badge")
    PROFILE_ICON = (By.XPATH, "//span[contains(@class, 'k-i-user')]/ancestor::span[contains(@class, 'k-menu-link')]")
    PROFILE_DROPDOWN_LINK = (By.XPATH, "//a[contains(@href, '/kendo-ui/eshop/Account/Profile')]")


    # 2. Metody wykonujące akcje
    def go_to_profile_icon(self):
        # Czekamy na ikonę i robimy Hover
        user_element = self.wait_for_visible(self.PROFILE_ICON)
        ActionChains(self.driver).move_to_element(user_element).perform()

    def click_profile_dropdown(self):
        # Klikamy w link profilu (BasePage zajmie się czekaniem na klikalność)
        self.click(self.PROFILE_DROPDOWN_LINK)

    def click_cart(self):
        self.click(self.SHOPPING_CART_BTN)