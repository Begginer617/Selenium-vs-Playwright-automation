from selenium.webdriver.common import by
from selenium.webdriver.common.by import By
from pages.selenium.base_page_selenium import BasePage


class LoginPage(BasePage):
    """
    Web element locators -  Errors
    """

    # --- BŁĘDY W PODSUMOWANIU
    # (Validation Summary)
    NAME_ERROR_VALIDATION_SUMMARY_LIST = (By.XPATH,
                                          "//div[contains(@class, 'k-validation-summary')]//li[contains(text(), 'First and Last name')]")
    EMAIL_ERROR_VALIDATION_SUMMARY_LIST = (By.XPATH,
                                           "//div[contains(@class, 'k-validation-summary')]//li[contains(text(), 'Email is required')]")
    PASS_ERROR_VALIDATION_SUMMARY_LIST = (By.XPATH,
                                          "//div[contains(@class, 'k-validation-summary')]//li[contains(text(), 'Please enter password')]")
    PASSWORD_REQUIREMENTS_VALIDATION_SUMMARY_LIST = (By.XPATH,
                                                     "//a[contains(text(), 'Your password must be at least 8 symbols ')]")

    # --- BŁĘDY POD INPUTAMI (Dół) ---
    NAME_ERROR_BOTTOM = (By.ID, "FirstAndLastName-error")
    EMAIL_ERROR_BOTTOM = (By.ID, "Email-error")
    PASS_ERROR_BOTTOM = (By.XPATH, "//span[@id='Password-error' and contains(text(), 'Please enter password)]")
    PLEASE_ENTER_FIRST_AND_LAST_NAME_SEPARATED_BY_A_SPACE_BOTTOM = (By.XPATH, "//span[@id='FirstAndLastName-error' and contains(text(), 'separated by a space')]")
    EMAIL_IS_NOT_VALID_EMAIL_BOTTOM = (By.XPATH, "//span[@id='Email-error' and text()='Email is not valid email']")
    PASSWORD_REQUIREMENTS_BOTTOM = (By.XPATH, "//span[@id='Password-error' and contains(text(), '8 symbols')]")

    """
     Web element locators - FORM Register and Login
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
        self.wait_for_visible(self.FIRST_AND_LAST_NAME_INPUT).clear()
        self.wait_for_visible(self.EMAIL_INPUT).clear()
        self.wait_for_visible(self.PASSWORD_INPUT).clear()
        self.click_register()

    def trigger_format_errors(self, incorrect_name, incorrect_email, short_password):
        """Metoda wpisuje błędne dane, aby wymusić komunikaty walidacji."""
        name_field = self.wait_for_visible(self.FIRST_AND_LAST_NAME_INPUT)
        name_field.clear()
        name_field.send_keys(incorrect_name)

        email_field = self.wait_for_visible(self.EMAIL_INPUT)
        email_field.clear()
        email_field.send_keys(incorrect_email)

        pass_field = self.wait_for_visible(self.PASSWORD_INPUT)
        pass_field.clear()
        pass_field.send_keys(short_password)

        self.click_register()
