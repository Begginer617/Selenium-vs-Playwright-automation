from selenium.webdriver.common import by
from selenium.webdriver.common.by import By
from pages.selenium.base_page_selenium import BasePage

class LoginPage(BasePage):
    """
    lOCALISATORS Errors
    """
    # --- BŁĘDY POD INPUTAMI (Dół) ---
    NAME_ERROR_BOTTOM = (By.ID, "FirstAndLastName-error")
    EMAIL_ERROR_BOTTOM = (By.ID, "Email-error")
    PASS_ERROR_BOTTOM = (By.ID, "Password-error")

    # --- BŁĘDY W PODSUMOWANIU (Góra - Twoja strzałka) ---
    # Szukamy konkretnego tekstu wewnątrz czerwonej ramki (Validation Summary)
    NAME_ERROR_TOP = (By.XPATH,
                      "//div[contains(@class, 'k-validation-summary')]//li[contains(text(), 'First and Last name')]")
    EMAIL_ERROR_TOP = (By.XPATH,
                       "//div[contains(@class, 'k-validation-summary')]//li[contains(text(), 'Email is required')]")
    PASS_ERROR_TOP = (By.XPATH,
                      "//div[contains(@class, 'k-validation-summary')]//li[contains(text(), 'Please enter password')]")


    """
    lOCALISATORS FORM Register and Login
    """
    LOGIN_BUTTON = (By.XPATH, "//a[@href='/kendo-ui/eshop/Account/Login']")
    REGISTER_SUBMIT_BUTTON = (By.XPATH, "//button[@type='submit']")
    FIRST_AND_LAST_NAME_INPUT = (By.XPATH, "//input[@id='FirstAndLastName']")
    EMAIL_INPUT = (By.XPATH, "//input[@id='Email']")
    PASSWORD_INPUT = (By.XPATH, "//input[@id='Password']")

    """
    Methodes
    """

    def trigger_required_errors(self):
        """Wywołuje błędy 'Email is required' itp. poprzez kliknięcie w pusty formularz."""
        self.wait_for_visible(self.NAME_INPUT).clear()
        self.wait_for_visible(self.EMAIL_INPUT).clear()
        self.wait_for_visible(self.PASSWORD_INPUT).clear()
        self.click_register()

    def trigger_format_errors(self, incorrect_name, incorrect_email, short_password):
        """Metoda wpisuje błędne dane, aby wymusić komunikaty walidacji."""
        name_field = self.wait_for_visible(self.NAME_INPUT)
        name_field.clear()
        name_field.send_keys(incorrect_name)

        email_field = self.wait_for_visible(self.EMAIL_INPUT)
        email_field.clear()
        email_field.send_keys(incorrect_email)

        pass_field = self.wait_for_visible(self.PASSWORD_INPUT)
        pass_field.clear()
        pass_field.send_keys(short_password)

        self.click_register()





