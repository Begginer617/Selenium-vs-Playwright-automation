from selenium.webdriver.common.by import By
from pages.selenium.base_page_selenium import BasePage


class RegistrationPage(BasePage):
    """
    Web element locators - Registration - Errors Registration
    """

    # Validation summary errors

    # State: empty fields
    EMPTY_FIRST_AND_LAST_NAME_VALIDATION_SUMMARY_LIST = (By.XPATH, "//li[contains(., 'First and Last name')]")
    EMPTY_EMAIL_ERROR_VALIDATION_SUMMARY_LIST = (By.XPATH, "//li[contains(., 'Email is required')]")

    EMPTY_PASSWORD_ERROR_VALIDATION_SUMMARY_LIST = (By.XPATH, "//li[contains(., 'Please enter password')]")

    # State: wrong formats
    FIRST_AND_LAST_NAME_SEPARATED_BY_A_SPACE_VALIDATION_SUMMARY_LIST = (By.XPATH,
                                                                        "//a[@data-field='FirstAndLastName' and contains(text(), 'separated by a space')]")
    EMAIL_IS_NOT_VALID_VALIDATION_SUMMARY_LIST = (By.XPATH,
                                                  "//a[@data-field='Email' and text()='Email is not valid email']")
    PASSWORD_REQUIREMENTS_VALIDATION_SUMMARY_LIST = (By.XPATH,
                                                     "//a[@data-field='Password' and contains(text(), '8 symbols')]")

    """
    Web element locators - Registration - errors under inputs
    """
    # --- Errors under inputs ---
    # State: empty fields errors
    # 1
    EMPTY_FIRST_AND_LAST_NAME_BOTTOM = (By.ID, "FirstAndLastName-error")
    # 2
    EMPTY_EMAIL_ERROR_BOTTOM = (By.ID, "Email-error")
    # 3
    EMPTY_PASSWORD_ERROR_BOTTOM = (By.XPATH,
                                   "//span[@id='Password-error' and contains(text(), 'Please enter password')]")

    # State: wrong format errors
    # 4
    FIRST_AND_LAST_NAME_SEPARATED_BY_A_SPACE_BOTTOM = (By.XPATH,
                                                       "//span[@id='FirstAndLastName-error' and contains(text(), 'separated by a space')]")
    # 5
    EMAIL_IS_NOT_VALID_EMAIL_BOTTOM = (By.XPATH, "//span[@id='Email-error' and text()='Email is not valid email']")
    # 6
    PASSWORD_REQUIREMENTS_BOTTOM = (By.XPATH, "//span[@id='Password-error' and contains(text(), '8 symbols')]")

    """
     Web element locators - FORM Register and Login
    """

    FIRST_AND_LAST_NAME_INPUT = (By.ID, "FirstAndLastName")
    EMAIL_INPUT = (By.ID, "Email")
    PASSWORD_INPUT = (By.ID, "Password")

    """
    Web element locators - buttons
    """

    LOGIN_BUTTON_REGISTRATION = (By.XPATH, "//a[@href='/kendo-ui/eshop/Account/Login']")
    REGISTER_SUBMIT_BUTTON = (By.XPATH, "//button[@type='submit']")

    """
    Methods
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

    def open_registration_url(self):
        self.open("https://demos.telerik.com/kendo-ui/eshop/Account/Register")

    def get_required_error_elements(self):
        return {
            "summary": {
                "name": self.wait_for_visible(self.EMPTY_FIRST_AND_LAST_NAME_VALIDATION_SUMMARY_LIST),
                "email": self.wait_for_visible(self.EMPTY_EMAIL_ERROR_VALIDATION_SUMMARY_LIST),
                "password": self.wait_for_visible(self.EMPTY_PASSWORD_ERROR_VALIDATION_SUMMARY_LIST),
            },
            "inline": {
                "name": self.wait_for_visible(self.EMPTY_FIRST_AND_LAST_NAME_BOTTOM),
                "email": self.wait_for_visible(self.EMPTY_EMAIL_ERROR_BOTTOM),
                "password": self.wait_for_visible(self.EMPTY_PASSWORD_ERROR_BOTTOM),
            },
        }

    def assert_required_errors(self):
        required_errors = self.get_required_error_elements()
        for element in required_errors["summary"].values():
            assert element.is_displayed()
        assert required_errors["inline"]["name"].is_displayed()
        assert "Email is required" in required_errors["inline"]["email"].text
        assert "Please enter password" in required_errors["inline"]["password"].text

    def get_format_error_elements(self):
        return {
            "summary": {
                "name": self.wait_for_visible(self.FIRST_AND_LAST_NAME_SEPARATED_BY_A_SPACE_VALIDATION_SUMMARY_LIST),
                "email": self.wait_for_visible(self.EMAIL_IS_NOT_VALID_VALIDATION_SUMMARY_LIST),
                "password": self.wait_for_visible(self.PASSWORD_REQUIREMENTS_VALIDATION_SUMMARY_LIST),
            },
            "inline": {
                "name": self.wait_for_visible(self.FIRST_AND_LAST_NAME_SEPARATED_BY_A_SPACE_BOTTOM),
                "email": self.wait_for_visible(self.EMAIL_IS_NOT_VALID_EMAIL_BOTTOM),
                "password": self.wait_for_visible(self.PASSWORD_REQUIREMENTS_BOTTOM),
            },
        }

    def assert_format_errors(self):
        format_errors = self.get_format_error_elements()
        for element in format_errors["summary"].values():
            assert element.is_displayed()
        assert "separated by a space" in format_errors["inline"]["name"].text
        assert "not valid email" in format_errors["inline"]["email"].text
        assert "8 symbols" in format_errors["inline"]["password"].text
