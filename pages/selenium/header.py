from selenium.webdriver.common.by import By
from pages.selenium.base_page import BasePage
from selenium.webdriver.common.action_chains import ActionChains


class Header(BasePage):
    """
     lOCALISATORS HEADER
     """

    SHOPPING_CART_BUTTON = driver.find_element(By.XPATH, "//a[contains(@href, 'ShoppingCart')]")
    SHOPPING_CART_COUNT = driver.find_element(By.XPATH, "//span[@id='shopping-cart-badge']")
    PROFILE_ICONE = driver.find_element(By.XPATH,
                                        "//span[contains(@class, 'k-i-user')]/ancestor::span[contains(@class, 'k-menu-link')]")
    PROFILE_ICONE_DROP_DOWN = driver.find_element(By.XPATH, "//a[contains(@href, '/kendo-ui/eshop/Account/Profile')]")


def go_to_profile_icon(self):
    user_element = self.wait_for_visible(self.PROFILE_ICONE)
    ActionChains(self.driver).move_to_element(user_element).perform()


