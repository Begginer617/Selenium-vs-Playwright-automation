from selenium.webdriver.common.by import By
from pages.selenium.base_page_selenium import BasePage
from selenium.webdriver.common.keys import Keys


class LoginPage(BasePage):
    ADMIN_TEST_USER_EMAIL = "jaxons.danniels@company.com"
    ADMIN_TEST_USER_PASS = "User1234"

    """
    Login page locators
    """
    LOGIN_FIELD = (By.ID, "Email")
    PASSWORD_FIELD = (By.ID, "Password")
    LOGIN_BUTTON = (By.CSS_SELECTOR, ".k-form-submit")
    """
    Methodes type + click from BasePage
    """



    def login_as_admin(self):
        # Wpisujemy maila
        self.type(self.LOGIN_FIELD, self.ADMIN_TEST_USER_EMAIL)
        # Wpisujemy hasło
        self.type(self.PASSWORD_FIELD, self.ADMIN_TEST_USER_PASS)

        # Zamiast klikać w przycisk, który może być zasłonięty popupem:
        # Pobieramy pole hasła i uderzamy w ENTER
        password_element = self.driver.find_element(*self.PASSWORD_FIELD)
        password_element.send_keys(Keys.ENTER)


