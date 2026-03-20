import allure


class BasePage:

    def __init__(self, page):
        self.page = page

    def click(self, selector):
        self.page.locator(selector).click()

    def type(self, selector, text):
        self.page.locator(selector).fill(text)

    def get_text(self, selector):
        return self.page.locator(selector).inner_text()

    def open(self, url):
        self.page.goto(url)

    def screenshot(self, name="screenshot"):
        allure.attach(
            self.page.screenshot(),
            name=name,
            attachment_type=allure.attachment_type.PNG
        )
