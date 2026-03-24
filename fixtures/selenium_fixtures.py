import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


@pytest.fixture
def driver():
    options = Options()

    # --- DODAJ TE LINIE, ABY WYŁĄCZYĆ OKNO "ZMIEŃ HASŁO" ---
    prefs = {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False
    }
    options.add_experimental_option("prefs", prefs)
    # -------------------------------------------------------

    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    yield driver
    driver.quit()