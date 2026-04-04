import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import allure


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
        # Zmieniamy url_to_be na url_contains
        return self.wait.until(EC.url_contains(url))

    def wait_for_all_visible(self, locator):
        return self.wait.until(EC.visibility_of_all_elements_located(locator))


    # ---------- ACTIONS ----------
    def click(self, locator):
        try:
            self.wait_for_clickable(locator).click()
        except TimeoutException:
            self._attach_screenshot("click_error")
            raise

    def type(self, locator, text):
        try:
            element = self.wait_for_visible(locator)
            element.clear()
            element.send_keys(text)
        except TimeoutException:
            self._attach_screenshot("type_error")
            raise

    def get_text(self, locator):
        try:
            return self.wait_for_visible(locator).text
        except TimeoutException:
            self._attach_screenshot("get_text_error")
            raise

    def open(self, url):
        self.driver.get(url)
        time.sleep(2)

    def scroll_to(self, locator):
        element = self.wait_for_visible(locator)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)

    # ---------- ALLURE ----------
    def _attach_screenshot(self, name):
        allure.attach(
            self.driver.get_screenshot_as_png(),
            name=name,
            attachment_type=allure.attachment_type.PNG
        )

    def click_with_js(self, locator):
        element = self.driver.find_element(*locator)
        self.driver.execute_script("arguments[0].click();", element)