import pytest
import allure
from pages.playwright.header_page_playwright import HeaderPagePw
from pages.playwright.home_page_playwright import HomePagePw
from pages.playwright.login_page_playwright import LoginPagePw
from pages.playwright.products_page_playwright import ProductPagePw
from pages.playwright.registration_page_playwright import RegistrationPagePw


@pytest.fixture
def home_page_pw(page):
    return HomePagePw(page)


@pytest.fixture
def login_page_pw(page):
    return LoginPagePw(page)


@pytest.fixture
def header_page_pw(page):
    return HeaderPagePw(page)


@pytest.fixture
def product_page_pw(page):
    return ProductPagePw(page)


@pytest.fixture
def registration_page_pw(page):
    return RegistrationPagePw(page)


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "viewport": {"width": 1920, "height": 1080},
        "base_url": "https://demos.telerik.com/kendo-ui/eshop"
    }


@pytest.fixture(scope="session")
def browser_type_launch_args():
    return {
        "headless": False,
        "slow_mo": 5,
        "args": ["--window-size", "--window-size=1920,1080"]
    }


@pytest.fixture(scope="session")
def browser_context_args():
    return {
        # viewport=None lets the browser control window size
        "viewport": None,
        "base_url": "https://demos.telerik.com/kendo-ui/eshop"
    }


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    _ = call

    if rep.when == "call" and rep.failed:
        # Get the test's `page` fixture
        page = item.funcargs.get("page")
        if page:
            try:
                # full_page=False captures the viewport only
                # timeout=5000 avoids hanging forever
                screenshot = page.screenshot(full_page=False, timeout=5000)
                allure.attach(
                    screenshot,
                    name="failure_screenshot_pw",
                    attachment_type=allure.attachment_type.PNG
                )
            except Exception as e:
                print(f"\n[Allure] Failed to capture failure screenshot: {e}")
