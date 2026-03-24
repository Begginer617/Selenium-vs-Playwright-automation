import pytest
import allure
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pages.selenium.home_page_selenium import HomePage
from pages.selenium.login_page_selenium import LoginPage
from pages.selenium.registration_page_selenium import RegistrationPage


@pytest.fixture
def driver():
    # 1. Konfiguracja opcji (blokada okna haseł)
    options = Options()
    prefs = {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False
    }
    options.add_experimental_option("prefs", prefs)

    # 2. Inicjalizacja drivera
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()

    yield driver  # Test ignition

    # 3. Sprzątanie
    driver.quit()


# --- FIXTURY STRON ---
# Dzięki temu w testach wpisujesz tylko nazwę w nawiasie, np. def test(login_page):
@pytest.fixture
def registration_page(driver):
    return RegistrationPage(driver)


@pytest.fixture
def home_page_selenium(driver):
    return HomePage(driver)


@pytest.fixture
def login_page(driver):
    return LoginPage(driver)


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