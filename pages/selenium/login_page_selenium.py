from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from pages.selenium.base_page_selenium import BasePage
from selenium.webdriver.common.keys import Keys
import time


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
        # 1. Standardowe wpisywanie danych
        self.type(self.LOGIN_FIELD, self.ADMIN_TEST_USER_EMAIL)
        self.type(self.PASSWORD_FIELD, self.ADMIN_TEST_USER_PASS)

        # 2. Logowanie Enterem (Twój dobry pomysł)
        password_element = self.driver.find_element(*self.PASSWORD_FIELD)
        password_element.send_keys(Keys.ENTER)

        # 3. FIX na popup Chrome:
        # Dajemy mu pół sekundy na wyskoczenie i "bijemy" w ESCAPE
        time.sleep(0.5)
        try:
            # Wysyłamy ESC do całego okna przeglądarki
            ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()
            # Dodatkowo klikamy w tło strony, żeby zdjąć focus z popupu
            self.driver.find_element(By.TAG_NAME, "body").click()
        except:
            pass # Jeśli popupu nie było, po prostu jedziemy dalej

        #4. Wejście na stronę główną sklepu - home page
            self.open("https://demos.telerik.com/kendo-ui/eshop")



