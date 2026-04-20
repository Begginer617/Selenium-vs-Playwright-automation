import contextlib
import allure
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Telerik eShop: navigate here before clearing so cookies/storage/CDP target this origin.
ESHOP_ENTRY_URL = "https://demos.telerik.com/kendo-ui/eshop/"
ESHOP_CDP_ORIGIN = "https://demos.telerik.com"

# --- IMPORTY TWOICH STRON ---
from pages.selenium.header_page_selenium import HeaderPage
from pages.selenium.home_page_selenium import HomePage
from pages.selenium.login_page_selenium import LoginPage
from pages.selenium.registration_page_selenium import RegistrationPage
from pages.selenium.products_page_selenium import ProductsPage


# --- Driver factory ---
class DriverFactory:
    @staticmethod
    def get_driver(run_remote, options):
        if run_remote:
            # Docker/remote execution.
            executor_url = "http://localhost:4444/wd/hub"
            driver = webdriver.Remote(
                command_executor=executor_url,
                options=options
            )
        else:
            # Local execution.
            driver = webdriver.Chrome(options=options)
        return driver


# --- Pytest CLI options ---
def pytest_addoption(parser):
    # Allow Docker/remote execution toggle from CLI.
    parser.addoption("--remote", action="store", default="false", help="Run on Docker: true or false")


# --- Main Selenium WebDriver fixture ---
@pytest.fixture(scope="session")
def driver(request):
    # 1. Read runtime options from CLI.
    remote_opt = request.config.getoption("--remote").lower() == "true"

    # 2. Configure Chrome options.
    options = Options()

    # Disable password/pop-up features that can interfere with automation.
    options.add_argument("--disable-features=PasswordLeakDetection,SafeBrowsing")
    options.add_argument("--disable-save-password-bubble")
    options.add_argument("--disable-notifications")
    options.add_argument("--guest")
    options.page_load_strategy = "eager"
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-renderer-backgrounding")
    options.add_argument("--disable-backgrounding-occluded-windows")

    # Improve stability in containerized/virtualized Linux.
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # Hide automation extensions/flags.
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    # Profile preferences.
    prefs = {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "autofill.profile_enabled": False
    }
    options.add_experimental_option("prefs", prefs)

    # 3. Initialize driver.
    driver = DriverFactory.get_driver(run_remote=remote_opt, options=options)
    driver.set_page_load_timeout(4)
    driver.implicitly_wait(3)
    with contextlib.suppress(Exception):
        driver.maximize_window()
    yield driver

    # 4. Teardown.
    driver.quit()

# --- Per-test browser-state reset on shared driver ---
@pytest.fixture(autouse=True)
def reset_browser_state(driver):
    # Keep tests isolated while reusing one browser instance for speed.
    with contextlib.suppress(Exception):
        driver.get(ESHOP_ENTRY_URL)
    with contextlib.suppress(Exception):
        driver.delete_all_cookies()
    with contextlib.suppress(Exception):
        driver.execute_script(
            "try { localStorage.clear(); } catch (e) {}"
            "try { sessionStorage.clear(); } catch (e) {}"
        )
    # Chromium: clear IndexedDB, cache storage, etc. for the origin
    with contextlib.suppress(Exception):
        driver.execute_cdp_cmd(
            "Storage.clearDataForOrigin",
            {"origin": ESHOP_CDP_ORIGIN, "storageTypes": "all"},
        )
    with contextlib.suppress(Exception):
        driver.execute_cdp_cmd("Network.clearBrowserCache", {})
    yield


# --- FIXTURY STRON Selenium (Page Objects) ---
@pytest.fixture
def registration_page_selenium(driver):
    return RegistrationPage(driver)


@pytest.fixture
def home_page_selenium(driver):
    return HomePage(driver)


@pytest.fixture
def login_page_selenium(driver):
    return LoginPage(driver)


@pytest.fixture
def header_page_selenium(driver):
    return HeaderPage(driver)


@pytest.fixture
def product_page_selenium(driver):
    return ProductsPage(driver)


# --- Automatic Allure screenshots on test failure ---
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    # Capture screenshot only when test fails in call phase.
    if rep.when == "call" and rep.failed:
        if "driver" in item.fixturenames:
            driver = item.funcargs.get("driver")
            if driver:
                try:
                    allure.attach(
                        driver.get_screenshot_as_png(),
                        name="failure_screenshot_selenium",
                        attachment_type=allure.attachment_type.PNG
                    )
                except Exception as e:
                    print(f"\n[Allure] Failed to capture screenshot: {e}")