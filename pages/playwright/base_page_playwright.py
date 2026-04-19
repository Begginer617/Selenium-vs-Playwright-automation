import re
import time
import allure
from playwright.sync_api import Page, expect

class BasePagePw:
    def __init__(self, page: Page, timeout_ms: int = 8000):
        self.page = page
        self.timeout_ms = timeout_ms
        self._log("STEP", "Initializing page object and viewport 1920x1080")
        self.page.set_viewport_size({"width": 1920, "height": 1080})

    def _log(self, level: str, message: str):
        print(f"[POM][{level}] {message}")

    def log_step(self, message: str):
        self._log("STEP", message)

    def log_info(self, message: str):
        self._log("INFO", message)

    def log_assert(self, message: str):
        self._log("ASSERT", message)

    def log_done(self, message: str):
        self._log("DONE", message)

    def log_warn(self, message: str):
        self._log("WARN", message)

    def log_error(self, message: str):
        self._log("ERROR", message)

    def open(self, url: str):
        self._log("STEP", f"Navigating to URL: {url}")
        self.safe_goto(url, wait_until="domcontentloaded")

    def safe_goto(self, url: str, wait_until: str = "domcontentloaded", retries: int = 3):
        last_exception = None
        for attempt in range(retries):
            try:
                self.page.goto(url, wait_until=wait_until)
                return
            except Exception as exc:  # Playwright Timeout/Error classes are runtime-provided.
                last_exception = exc
                if attempt < retries - 1:
                    self.log_warn(
                        f"Navigation failed (attempt {attempt + 1}/{retries}) for '{url}': {exc}. Retrying..."
                    )
                    time.sleep(0.4)
                    continue
        self.log_error(f"Navigation failed after {retries} attempts: {url}")
        raise last_exception

    def click(self, selector: str):
        self._log("STEP", f"Clicking element: {selector}")
        locator = self.page.locator(selector)
        expect(locator).to_be_visible(timeout=self.timeout_ms)
        locator.click()

    def js_click(self, selector: str):
        self._log("STEP", f"Executing JS click on element: {selector}")
        locator = self.page.locator(selector)
        # JS click is used as fallback also for covered/hidden nodes.
        expect(locator).to_have_count(1, timeout=self.timeout_ms)
        locator.evaluate("el => el.click()")

    def type(self, selector: str, text: str):
        self._log("STEP", f"Typing text into field: {selector}")
        locator = self.page.locator(selector)
        expect(locator).to_be_visible(timeout=self.timeout_ms)
        locator.fill(text)

    def get_title(self):
        title = self.page.title()
        self._log("INFO", f"Retrieved page title: '{title}'")
        return title

    def wait_for_visible(self, selector: str):
        locator = self.page.locator(selector)
        expect(locator).to_be_visible(timeout=self.timeout_ms)
        return locator

    def wait_for_url(self, expected_url_fragment: str):
        # Use regex "contains" semantics to avoid fragile glob-base_url interactions.
        expect(self.page).to_have_url(
            re.compile(re.escape(expected_url_fragment)),
            timeout=self.timeout_ms,
        )

    def screenshot(self, name="screenshot"):
        self._log("INFO", f"Taking screenshot: {name}")
        allure.attach(
            self.page.screenshot(),
            name=name,
            attachment_type=allure.attachment_type.PNG
        )