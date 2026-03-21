import pytest
from utils.driver_factory import DriverFactory


@pytest.fixture
def driver():
    # SETUP: Tu tworzymy połączenie z Dockerem
    driver = DriverFactory.get_driver("chrome")

    yield driver  # Tu "zatrzymuje się" fixture i wykonuje się Twój TEST

    # TEARDOWN: To wykona się ZAWSZE po teście (nawet jak test padnie)
    if driver:
        driver.quit()