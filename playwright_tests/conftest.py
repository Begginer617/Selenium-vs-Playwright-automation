import pytest
import allure
from pages.playwright.header_page_playwright import HeaderPagePw
from pages.playwright.home_page_playwright import HomePagePw
from pages.playwright.login_page_playwright import LoginPagePw
from pages.playwright.products_page_playwright import ProductsPagePw
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
def products_page_pw(page):
    return ProductsPagePw(page)


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


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        # Pobieramy fixturę 'page' z testu
        page = item.funcargs.get("page")
        if page:
            try:
                # full_page=False robi screena tylko tego, co widać (bezpieczniejsze)
                # timeout=5000 sprawi, że nie będziemy czekać w nieskończoność
                screenshot = page.screenshot(full_page=False, timeout=5000)
                allure.attach(
                    screenshot,
                    name="failure_screenshot_pw",
                    attachment_type=allure.attachment_type.PNG
                )
            except Exception as e:
                print(f"\n[Błąd Allure] Nie udało się wykonać zrzutu ekranu: {e}")
