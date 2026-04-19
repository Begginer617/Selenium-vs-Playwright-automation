import time
import allure
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    NoSuchElementException,
    StaleElementReferenceException,
    TimeoutException,
    WebDriverException,
)


class BasePage:

    def __init__(self, driver, timeout=8, poll_frequency=0.2):
        self.driver = driver
        self.default_timeout = timeout
        self.poll_frequency = poll_frequency
        self.wait = self._build_wait(timeout)

    def _build_wait(self, timeout):
        return WebDriverWait(
            self.driver,
            timeout,
            poll_frequency=self.poll_frequency,
            ignored_exceptions=(NoSuchElementException, StaleElementReferenceException),
        )

    def _wait(self, condition, timeout=None):
        effective_timeout = timeout if timeout is not None else self.default_timeout
        return self._build_wait(effective_timeout).until(condition)

    def _log(self, level, message):
        print(f"[POM][{level}] {message}")

    def log_step(self, message):
        self._log("STEP", message)

    def log_info(self, message):
        self._log("INFO", message)

    def log_assert(self, message):
        self._log("ASSERT", message)

    def log_done(self, message):
        self._log("DONE", message)

    def log_warn(self, message):
        self._log("WARN", message)

    # Backward-compatible alias used in some page objects.
    def log_warning(self, message):
        self.log_warn(message)

    def log_error(self, message):
        self._log("ERROR", message)

    # ---------- WAIT HELPERS ----------
    def wait_for_visible(self, locator, timeout=None):
        return self._wait(EC.visibility_of_element_located(locator), timeout)

    def wait_for_clickable(self, locator, timeout=None):
        return self._wait(EC.element_to_be_clickable(locator), timeout)

    def wait_for_url(self, url, timeout=None):
        return self._wait(EC.url_contains(url), timeout)

    def wait_for_all_visible(self, locator, timeout=None):
        return self._wait(EC.visibility_of_all_elements_located(locator), timeout)

    def wait_for_presence(self, locator, timeout=None):
        return self._wait(EC.presence_of_element_located(locator), timeout)

    def wait_for_all_present(self, locator, timeout=None):
        return self._wait(EC.presence_of_all_elements_located(locator), timeout)

    def wait_for_page_load(self, timeout=10):
        try:
            self._build_wait(timeout).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
        except TimeoutException:
            # Do not fail hard here; some apps remain usable while background scripts are still running.
            self._log("WARN", "Timed out waiting for document.readyState='complete'; continuing test.")

    # ---------- ACTIONS ----------
    def click(self, locator):
        self.wait_for_clickable(locator).click()

    def safe_click(self, locator, retries=2):
        last_exception = None
        for attempt in range(retries):
            try:
                self.wait_for_clickable(locator).click()
                return
            except (TimeoutException, StaleElementReferenceException, ElementClickInterceptedException) as exc:
                last_exception = exc
                if attempt < retries - 1:
                    time.sleep(0.2)
                    continue
        self._attach_screenshot("safe_click_error")
        raise TimeoutException(f"Failed to click element after {retries} attempts: {locator}") from last_exception

    def type(self, locator, text):
        element = self.wait_for_visible(locator)
        element.clear()
        element.send_keys(text)

    def get_text(self, locator):
        return self.wait_for_visible(locator).text

    def open(self, url, retries=3):
        last_exception = None
        for attempt in range(retries):
            try:
                self.driver.get(url)
                self.wait_for_page_load(timeout=10)
                return
            except (TimeoutException, WebDriverException) as exc:
                last_exception = exc
                self.log_warn(
                    f"Navigation attempt {attempt + 1}/{retries} failed for '{url}': {exc}"
                )
                # Renderer timeout can leave Chrome in transient broken state; stop pending load and retry.
                try:
                    self.driver.execute_script("window.stop();")
                except Exception:
                    pass
                try:
                    # Reset page context before next attempt to reduce repeated renderer stalls.
                    self.driver.get("about:blank")
                except Exception:
                    pass
                if attempt < retries - 1:
                    time.sleep(1)
                    continue
        raise last_exception

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
