import pytest
import allure
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pages.selenium.header_page_selenium import HeaderSeleniumPage
from pages.selenium.home_page_selenium import HomePage
from pages.selenium.login_page_selenium import LoginPage
from pages.selenium.registration_page_selenium import RegistrationPage


@pytest.fixture
def driver():
    options = Options()

    # 1. Całkowite wyłączenie systemów pomocniczych Chrome
    options.add_argument("--disable-features=PasswordLeakDetection,SafeBrowsing")
    options.add_argument("--disable-component-update")  # Blokuje aktualizacje modułów bezpieczeństwa
    options.add_argument("--disable-save-password-bubble")
    options.add_argument("--disable-notifications")
    options.page_load_strategy = 'eager'


    # 2. Tryb "Guest" lub "Incognito" - to zazwyczaj zabija managera haseł
    options.add_argument("--guest")

    # 3. Ukrycie automatyzacji
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    # 4. Preferencje (agresywne)
    prefs = {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "autofill.profile_enabled": False,
        "password_manager_leak_detection": False
    }
    options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(options=options)
    driver.maximize_window()

    yield driver
    driver.quit()


# --- FIXTURY STRON ---
@pytest.fixture
def registration_page(driver):
    return RegistrationPage(driver)


@pytest.fixture
def home_page_selenium(driver):
    return HomePage(driver)


@pytest.fixture
def login_page(driver):
    return LoginPage(driver)


@pytest.fixture
def header_page_selenium(driver):
    return HeaderSeleniumPage(driver)


# --- AUTOMATYCZNE SCREENSHOTY W ALLURE ---
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call" and rep.failed:
        if "driver" in item.fixturenames:
            driver = item.funcargs['driver']
            allure.attach(
                driver.get_screenshot_as_png(),
                name="screenshot_on_failure",
                attachment_type=allure.attachment_type.PNG
            )