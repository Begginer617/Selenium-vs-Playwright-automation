from selenium.webdriver.common.by import By
from pages.selenium.base_page_selenium import BasePage


class LoginPage(BasePage):
    """
    Web element locators - Registration - Errors Registration
    """

    # --- BŁĘDY W PODSUMOWANIU
    # (Validation Summary)

    # Stan: Empty fields
    EMPTY_FIRST_AND_LAST_NAME_VALIDATION_SUMMARY_LIST = (By.XPATH, "//li[contains(., 'First and Last name')]")
    EMPTY_EMAIL_ERROR_VALIDATION_SUMMARY_LIST = (By.XPATH, "//li[contains(., 'Email is required')]")

    EMPTY_PASSWORD_ERROR_VALIDATION_SUMMARY_LIST = (By.XPATH, "//li[contains(., 'Please enter password')]")

    # Stan: Wrong Formats
    FIRST_AND_LAST_NAME_SEPARATED_BY_A_SPACE_VALIDATION_SUMMARY_LIST = (By.XPATH,
                                                                        "//a[@data-field='FirstAndLastName' and contains(text(), 'separated by a space')]")
    EMAIL_IS_NOT_VALID_VALIDATION_SUMMARY_LIST = (By.XPATH,
                                                  "//a[@data-field='Email' and text()='Email is not valid email']")
    PASSWORD_REQUIREMENTS_VALIDATION_SUMMARY_LIST = (By.XPATH,
                                                     "//a[@data-field='Password' and contains(text(), '8 symbols')]")

    """
    Web element locators - Registration - Errors under inputs (Dół)
    """
    # --- BŁĘDY POD INPUTAMI (Dół) ---
    # Stan: Empty fields
    EMPTY_FIRST_AND_LAST_NAME_BOTTOM = (By.ID, "FirstAndLastName-error")
    EMPTY_EMAIL_ERROR_BOTTOM = (By.ID, "Email-error")
    EMPTY_PASSWORD_ERROR_BOTTOM = (By.XPATH,
                                   "//span[@id='Password-error' and contains(text(), 'Please enter password')]")

    # Stan: Wrong Formats
    FIRST_AND_LAST_NAME_SEPARATED_BY_A_SPACE_BOTTOM = (By.XPATH,
                                                       "//span[@id='FirstAndLastName-error' and contains(text(), 'separated by a space')]")
    EMAIL_IS_NOT_VALID_EMAIL_BOTTOM = (By.XPATH, "//span[@id='Email-error' and text()='Email is not valid email']")
    PASSWORD_REQUIREMENTS_BOTTOM = (By.XPATH, "//span[@id='Password-error' and contains(text(), '8 symbols')]")

    """
     Web element locators - FORM Register and Login
    """

    FIRST_AND_LAST_NAME_INPUT = (By.ID, "FirstAndLastName")
    EMAIL_INPUT = (By.ID, "Email")
    PASSWORD_INPUT = (By.ID, "Password")

    """
    Web element locators - Buttons login page
    """

    LOGIN_BUTTON_REGISTRATION = (By.XPATH, "//a[@href='/kendo-ui/eshop/Account/Login']")
    REGISTER_SUBMIT_BUTTON = (By.XPATH, "//button[@type='submit']")

    # """
    # Login page locators
    # """
    # LOGIN_FIELD = (By.XPATH, "//input[@data-role='textbox' and @id='Email']")
    # PASSWORD_FIELD = (By.XPATH, "//input[@data-role='textbox' and @type='password']")
    # LOGIN_BUTTON = (By.XPATH, "//button[@type='submit']")

    """
    Methodes
    """

    def click_register(self):
        self.wait_for_clickable(self.REGISTER_SUBMIT_BUTTON).click()

    def trigger_required_errors(self):
        self.wait_for_visible(self.FIRST_AND_LAST_NAME_INPUT).clear()
        self.wait_for_visible(self.EMAIL_INPUT).clear()
        self.wait_for_visible(self.PASSWORD_INPUT).clear()
        self.click_register()

    def trigger_format_errors(self, incorrect_name, incorrect_email, short_password):
        self.wait_for_visible(self.FIRST_AND_LAST_NAME_INPUT).send_keys(incorrect_name)
        self.wait_for_visible(self.EMAIL_INPUT).send_keys(incorrect_email)
        self.wait_for_visible(self.PASSWORD_INPUT).send_keys(short_password)
        self.click_register()

    def registration_url(self, driver):
        self.driver.get("https://demos.telerik.com/kendo-ui/eshop/Account/Register")


