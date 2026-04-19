from playwright.sync_api import Page, expect


class RegistrationPagePw:
    def __init__(self, page: Page):
        self.page = page

        # --- Validation summary errors ---
        self.EMPTY_FIRST_AND_LAST_NAME_VALIDATION_SUMMARY_LIST = "//li[contains(., 'First and Last name')]"
        self.EMPTY_EMAIL_ERROR_VALIDATION_SUMMARY_LIST = "//li[contains(., 'Email is required')]"
        self.EMPTY_PASSWORD_ERROR_VALIDATION_SUMMARY_LIST = "//li[contains(., 'Please enter password')]"

        self.FIRST_AND_LAST_NAME_SEPARATED_BY_A_SPACE_VALIDATION_SUMMARY_LIST = "//a[@data-field='FirstAndLastName' and contains(text(), 'separated by a space')]"
        self.EMAIL_IS_NOT_VALID_VALIDATION_SUMMARY_LIST = "//a[@data-field='Email' and text()='Email is not valid email']"
        self.PASSWORD_REQUIREMENTS_VALIDATION_SUMMARY_LIST = "//a[@data-field='Password' and contains(text(), '8 symbols')]"

        # --- Errors under inputs ---
        self.EMPTY_FIRST_AND_LAST_NAME_BOTTOM = "#FirstAndLastName-error"
        self.EMPTY_EMAIL_ERROR_BOTTOM = "#Email-error"
        self.EMPTY_PASSWORD_ERROR_BOTTOM = "//span[@id='Password-error' and contains(text(), 'Please enter password')]"

        self.FIRST_AND_LAST_NAME_SEPARATED_BY_A_SPACE_BOTTOM = "//span[@id='FirstAndLastName-error' and contains(text(), 'separated by a space')]"
        self.EMAIL_IS_NOT_VALID_EMAIL_BOTTOM = "//span[@id='Email-error' and text()='Email is not valid email']"
        self.PASSWORD_REQUIREMENTS_BOTTOM = "//span[@id='Password-error' and contains(text(), '8 symbols')]"

        # --- Form fields ---
        self.FIRST_AND_LAST_NAME_INPUT = "#FirstAndLastName"
        self.EMAIL_INPUT = "#Email"
        self.PASSWORD_INPUT = "#Password"
        self.REGISTER_SUBMIT_BUTTON = "//button[@type='submit']"

    def open_registration_url_pw(self):
        self.page.goto("https://demos.telerik.com/kendo-ui/eshop/Account/Register")

    def click_register_pw(self):
        # Use .first in case of duplicated submit buttons in the DOM.
        self.page.locator(self.REGISTER_SUBMIT_BUTTON).first.click()

    def trigger_required_errors_pw(self):
        # fill("") behaves like clear() + focus in Playwright.
        self.page.locator(self.FIRST_AND_LAST_NAME_INPUT).fill("")
        self.page.locator(self.EMAIL_INPUT).fill("")
        self.page.locator(self.PASSWORD_INPUT).fill("")
        self.click_register_pw()

    def trigger_format_errors_pw(self, incorrect_name, incorrect_email, short_password):
        self.page.locator(self.FIRST_AND_LAST_NAME_INPUT).fill(incorrect_name)
        self.page.locator(self.EMAIL_INPUT).fill(incorrect_email)
        self.page.locator(self.PASSWORD_INPUT).fill(short_password)
        self.click_register_pw()

    def is_visible_pw(self, selector):
        return self.page.locator(selector).first.is_visible()

    def get_text_pw(self, selector):
        return self.page.locator(selector).first.text_content()

    def expect_visible_pw(self, selector, timeout_ms=4000):
        expect(self.page.locator(selector).first).to_be_visible(timeout=timeout_ms)

    def expect_required_errors_pw(self):
        required_summary_selectors = [
            self.EMPTY_FIRST_AND_LAST_NAME_VALIDATION_SUMMARY_LIST,
            self.EMPTY_EMAIL_ERROR_VALIDATION_SUMMARY_LIST,
            self.EMPTY_PASSWORD_ERROR_VALIDATION_SUMMARY_LIST,
        ]
        required_inline_selectors = [
            self.EMPTY_FIRST_AND_LAST_NAME_BOTTOM,
            self.EMPTY_EMAIL_ERROR_BOTTOM,
            self.EMPTY_PASSWORD_ERROR_BOTTOM,
        ]

        for selector in required_summary_selectors + required_inline_selectors:
            self.expect_visible_pw(selector)

        expect(self.page.locator(self.EMPTY_EMAIL_ERROR_BOTTOM).first).to_contain_text("Email is required")
        expect(self.page.locator(self.EMPTY_PASSWORD_ERROR_BOTTOM).first).to_contain_text("Please enter password")

    def expect_format_errors_pw(self):
        format_summary_selectors = [
            self.FIRST_AND_LAST_NAME_SEPARATED_BY_A_SPACE_VALIDATION_SUMMARY_LIST,
            self.EMAIL_IS_NOT_VALID_VALIDATION_SUMMARY_LIST,
            self.PASSWORD_REQUIREMENTS_VALIDATION_SUMMARY_LIST,
        ]
        format_inline_selectors = [
            self.FIRST_AND_LAST_NAME_SEPARATED_BY_A_SPACE_BOTTOM,
            self.EMAIL_IS_NOT_VALID_EMAIL_BOTTOM,
            self.PASSWORD_REQUIREMENTS_BOTTOM,
        ]

        for selector in format_summary_selectors + format_inline_selectors:
            self.expect_visible_pw(selector)

        expect(self.page.locator(self.FIRST_AND_LAST_NAME_SEPARATED_BY_A_SPACE_BOTTOM).first).to_contain_text("separated by a space")
        expect(self.page.locator(self.EMAIL_IS_NOT_VALID_EMAIL_BOTTOM).first).to_contain_text("not valid email")
        expect(self.page.locator(self.PASSWORD_REQUIREMENTS_BOTTOM).first).to_contain_text("8 symbols")