import time
import allure
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class BasePage:

    def __init__(self, driver, timeout=5):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    # ---------- WAIT HELPERS ----------
    def wait_for_visible(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def wait_for_clickable(self, locator):
        return self.wait.until(EC.element_to_be_clickable(locator))

    def wait_for_url(self, url):
        return self.wait.until(EC.url_contains(url))

    def wait_for_all_visible(self, locator):
        return self.wait.until(EC.visibility_of_all_elements_located(locator))

    def wait_for_page_load(self, timeout=10):
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
        except TimeoutException:
            # Nie rzucamy błędu - często strona działa, mimo że jakiś skrypt w tle wisi
            print("Timeout czekania na status 'complete', kontynuuję test...")

    # ---------- ACTIONS ----------
    def click(self, locator):
        self.wait_for_clickable(locator).click()

    def safe_click(self, locator, retries=2):
        for _ in range(retries):
            try:
                self.wait_for_clickable(locator).click()
                return
            except Exception:
                time.sleep(0.3)
        self._attach_screenshot("safe_click_error")
        raise

    def type(self, locator, text):
        element = self.wait_for_visible(locator)
        element.clear()
        element.send_keys(text)

    def get_text(self, locator):
        self.wait_for_visible(locator).text

    def open(self, url):
        try:
            self.driver.get(url)
            # Zamiast twardego czekania, dajemy szansę na załadowanie się DOM
            self.wait_for_page_load(timeout=7)
        except TimeoutException:
            print(f"Strona {url} ładowała się zbyt długo.")

    def scroll_to(self, locator, offset=-150):
        element = self.wait_for_visible(locator)
        self.driver.execute_script(
            "window.scrollTo(0, arguments[0].getBoundingClientRect().top + window.scrollY + arguments[1]);",
            element,
            offset
        )

    def click_with_js(self, locator):
        element = self.wait_for_visible(locator)
        self.driver.execute_script("arguments[0].click();", element)

    def get_title(self):
        return self.driver.title

    # ---------- FIND HELPERS ----------
    def find(self, locator):
        return self.driver.find_element(*locator)

    def find_all(self, locator):
        return self.driver.find_elements(*locator)

    # ---------- ALLURE ----------
    def _attach_screenshot(self, name):
        allure.attach(
            self.driver.get_screenshot_as_png(),
            name=name,
            attachment_type=allure.attachment_type.PNG
        )
