import allure
from playwright.sync_api import Page

class BasePagePw:
    def __init__(self, page: Page):
        self.page = page
        print(f"[POM] Inicjalizacja strony - ustawianie viewport 1920x1080")
        self.page.set_viewport_size({"width": 1920, "height": 1080})

    def open(self, url: str):
        print(f"[POM] Nawigacja do URL: {url}")
        self.page.goto(url)

    def click(self, selector: str):
        print(f"[POM] Klikam element: {selector}")
        self.page.locator(selector).click()

    def js_click(self, selector: str):
        print(f"[POM] Wykonuję kliknięcie JS na elemencie: {selector}")
        self.page.locator(selector).evaluate("el => el.click()")

    def type(self, selector: str, text: str):
        print(f"[POM] Wpisuję tekst w pole {selector}")
        self.page.locator(selector).fill(text)

    def get_title(self):
        title = self.page.title()
        print(f"[POM] Pobrano tytuł strony: '{title}'")
        return title

    def screenshot(self, name="screenshot"):
        print(f"[POM] Wykonuję zrzut ekranu: {name}")
        allure.attach(
            self.page.screenshot(),
            name=name,
            attachment_type=allure.attachment_type.PNG
        )