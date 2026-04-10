from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from pages.selenium.base_page_selenium import BasePage


class HeaderPage(BasePage):
    # --- LOKATORY ---
    SHOPPING_CART_BTN = (By.XPATH, "//a[contains(@href, 'ShoppingCart')]")
    CATEGORIES_MENU = (By.XPATH, "//span[normalize-space()='Categories']")

    # Lokatory kategorii
    ACCESSORIES_LINK = (By.XPATH, "//a[contains(@class, 'k-menu-link') and normalize-space()='Accessories']")
    BIKES_LINK = (By.XPATH, "//a[contains(@class, 'k-menu-link') and normalize-space()='Bikes']")
    CLOTHES_LINK = (By.XPATH, "//a[contains(@class, 'k-menu-link') and normalize-space()='Clothes']")
    COMPONENTS_LINK = (By.XPATH, "//a[contains(@class, 'k-menu-link') and normalize-space()='Components']")

    # --- METODY PODSTAWOWE ---

    def click_cart(self):
        self.click(self.SHOPPING_CART_BTN)

    def open_home_page(self):
        """Przenosi użytkownika na stronę główną eshopu."""
        self.driver.get("https://demos.telerik.com/kendo-ui/eshop")

    def get_url(self):
        return self.driver.current_url




    # --- METODY KATEGORII ---

    def open_accessories_category(self):
        self._hover_and_click(self.ACCESSORIES_LINK)

    def open_bikes_category(self):
        self._hover_and_click(self.BIKES_LINK)

    def open_clothes_category(self):
        self._hover_and_click(self.CLOTHES_LINK)

    def open_components_category(self):
        self._hover_and_click(self.COMPONENTS_LINK)

    # Wspólna logika dla Hovera
    def _hover_and_click(self, locator):
        categories = self.wait_for_visible(self.CATEGORIES_MENU)
        # Przewijamy do menu, żeby było widoczne
        self.driver.execute_script("arguments[0].scrollIntoView(true);", categories)

        actions = ActionChains(self.driver)
        actions.move_to_element(categories).pause(0.5).perform()

        try:
            # Próbujemy normalnie kliknąć
            self.click(locator)
        except:
            # Jeśli menu zniknie lub Selenium 'zgubi' element - klikamy przez JS
            print(f"Standardowe kliknięcie zawiodło, używam JS dla: {locator}")
            element = self.driver.find_element(*locator)
            self.driver.execute_script("arguments[0].click();", element)


