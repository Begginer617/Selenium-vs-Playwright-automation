import pytest
from utils.driver_factory import DriverFactory
import allure
from pages.selenium.registration_page_selenium import RegistrationPage


@pytest.fixture
def driver():
    # SETUP: Tu tworzymy połączenie
    driver = DriverFactory.get_driver("chrome")

    yield driver  # TEST wykonuje się tutaj

    # TEARDOWN: To wykonuje się PO teście
    if driver:
        driver.quit()


@pytest.fixture
def registration_page(driver):
    """Tworzy obiekt strony logowania/rejestracji dla testów Selenium."""
    return RegistrationPage(driver)


@pytest.fixture
def login_page(driver):
    return  login_page(driver)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        # Sprawdzamy, czy driver był użyty w tym teście
        if "driver" in item.fixturenames:
            driver = item.funcargs['driver']
            allure.attach(
                driver.get_screenshot_as_png(),
                name="screenshot_on_failure",
                attachment_type=allure.attachment_type.PNG
            )