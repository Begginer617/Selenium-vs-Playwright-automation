from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from pages.selenium.base_page_selenium import BasePage

class HeaderSeleniumPage(BasePage):
    # 1. Lokatory
    SHOPPING_CART_BTN = (By.XPATH, "//a[contains(@href, 'ShoppingCart')]")
    SHOPPING_CART_COUNT = (By.ID, "shopping-cart-badge")
    PROFILE_ICON = (By.XPATH, "//span[contains(@class, 'k-i-user')]/ancestor::span[contains(@class, 'k-menu-link')]")
    PROFILE_DROPDOWN_LINK = (By.XPATH, "//a[contains(@href, '/kendo-ui/eshop/Account/Profile')]")
    CATEGORIES_MENU = (By.XPATH, "//span[normalize-space()='Categories']")
    ACCESSORIES_LINK = (By.XPATH, "//a[contains(@class, 'k-menu-link') and normalize-space()='Accessories']")

    # 2. Metody
    def go_to_profile_icon(self):
        user_element = self.wait_for_visible(self.PROFILE_ICON)
        ActionChains(self.driver).move_to_element(user_element).perform()

    def click_profile_dropdown(self):
        self.click(self.PROFILE_DROPDOWN_LINK)

    def click_cart(self):
        self.click(self.SHOPPING_CART_BTN)

    def open_accessories_category(self):
        # 1. Czekamy na Categories i najeżdżamy
        categories = self.wait_for_visible(self.CATEGORIES_MENU)

        # Przewijamy do elementu na wszelki wypadek
        self.driver.execute_script("arguments[0].scrollIntoView(true);", categories)

        # Wykonujemy hover z kliknięciem i przytrzymaniem (czasem pomaga w Kendo)
        actions = ActionChains(self.driver)
        actions.move_to_element(categories).click_and_hold(categories).pause(1).release().perform()

        # 2. Sprawdzamy widoczność Accessories
        # Jeśli tu wciąż wywala Timeout, spróbuj zamienić wait_for_visible na wait_for_clickable
        try:
            element = self.wait_for_visible(self.ACCESSORIES_LINK)
            element.click()
        except:
            # OSTATNIA DESKA RATUNKU: Kliknięcie przez JavaScript (ominie problem widoczności)
            print("Standardowe kliknięcie zawiodło, próbuję JS...")
            accessories = self.driver.find_element(*self.ACCESSORIES_LINK)
            self.driver.execute_script("arguments[0].click();", accessories)