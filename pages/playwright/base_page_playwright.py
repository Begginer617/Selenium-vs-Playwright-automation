import allure
from playwright.sync_api import Page


class BasePagePw:
    def __init__(self, page: Page):
        self.page = page

    def open(self, url: str):
        # Playwright automatycznie czeka na 'load' state
        self.page.goto(url)

    def click(self, selector: str):
        # Auto-waiting: Playwright sam sprawdzi czy element jest widoczny i klikalny
        self.page.locator(selector).click()

    def js_click(self, selector: str):
        """Klika w element bezpośrednio przez JavaScript, omijając sprawdzanie widoczności."""
        self.page.locator(selector).evaluate("el => el.click()")

    def type(self, selector: str, text: str):
        # .fill() jest lepsze niż .type() - czyści pole przed wpisaniem
        self.page.locator(selector).fill(text)

    def get_title(self):
        return self.page.title()
    def screenshot(self, name="screenshot"):
        allure.attach(
            self.page.screenshot(),
            name=name,
            attachment_type=allure.attachment_type.PNG
        )
