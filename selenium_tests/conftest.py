import allure
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# --- IMPORTY TWOICH STRON ---
from pages.selenium.header_page_selenium import HeaderSeleniumPage
from pages.selenium.home_page_selenium import HomePage
from pages.selenium.login_page_selenium import LoginPage
from pages.selenium.registration_page_selenium import RegistrationPage
from pages.selenium.products_page_selenium import ProductsPage



# --- ZINTEGROWANA FABRYKA DRIVERA ---
class DriverFactory:
    @staticmethod
    def get_driver(run_remote, options):
        if run_remote:
            # Ustawienia dla DOCKERA
            executor_url = "http://localhost:4444/wd/hub"
            driver = webdriver.Remote(
                command_executor=executor_url,
                options=options
            )
        else:
            # Ustawienia LOKALNE (Windows)
            driver = webdriver.Chrome(options=options)

        driver.maximize_window()
        return driver


# --- KONFIGURACJA PYTEST (FLAGI) ---
def pytest_addoption(parser):
    # Dodaje możliwość wpisania --remote true w konsoli
    parser.addoption("--remote", action="store", default="false", help="Run on Docker: true or false")


# --- GŁÓWNA FIXTURA DRIVERA ---
@pytest.fixture
def driver(request):
    # 1. Pobranie opcji z terminala
    remote_opt = request.config.getoption("--remote").lower() == "true"

    # 2. Konfiguracja zaawansowanych opcji Chrome (Twoje ustawienia)
    options = Options()

    # Blokowanie popupów i managera haseł
    options.add_argument("--disable-features=PasswordLeakDetection,SafeBrowsing")
    options.add_argument("--disable-save-password-bubble")
    options.add_argument("--disable-notifications")
    options.add_argument("--guest")
    options.page_load_strategy = 'eager'

    # Ukrycie automatyzacji
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    # Preferencje profilu
    prefs = {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "autofill.profile_enabled": False
    }
    options.add_experimental_option("prefs", prefs)

    # 3. Inicjalizacja przez Fabrykę
    driver = DriverFactory.get_driver(run_remote=remote_opt, options=options)

    yield driver

    # 4. Zamknięcie
    driver.quit()


# --- FIXTURY STRON (Page Objects) ---
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
    return HeaderSeleniumPage(driver)

@pytest.fixture
def product_page_selenium(driver):
    return ProductsPage(driver)




# --- AUTOMATYCZNE SCREENSHOTY DLA ALLURE W RAZIE BŁĘDU ---
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call" and rep.failed:
        if "driver" in item.fixturenames:
            driver = item.funcargs['driver']
            allure.attach(
                driver.get_screenshot_as_png(),
                name="failure_screenshot",
                attachment_type=allure.attachment_type.PNG
            )