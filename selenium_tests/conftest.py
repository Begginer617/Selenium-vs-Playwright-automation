import pytest
from utils.driver_factory import DriverFactory
import allure


@pytest.fixture
def driver():
    # SETUP: Tu tworzymy połączenie z Dockerem
    driver = DriverFactory.get_driver("chrome")

    yield driver  # Tu "zatrzymuje się" fixture i wykonuje się Twój TEST

    # TEARDOWN: To wykona się ZAWSZE po teście (nawet jak test padnie)
    if driver:
        driver.quit()

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # Wykonujemy test i sprawdzamy wynik
    outcome = yield
    rep = outcome.get_result()

    # Sprawdzamy, czy test się nie udał (failed)
    if rep.when == "call" and rep.failed:
        mode = "a" if "driver" in item.fixturenames else None
        if mode:
            # Wyciągamy drivera z testu
            driver = item.funcargs['driver']
            # Robimy zdjęcie i dołączamy do Allure
            allure.attach(
                driver.get_screenshot_as_png(),
                name="screenshot_on_failure",
                attachment_type=allure.attachment_type.PNG
            )