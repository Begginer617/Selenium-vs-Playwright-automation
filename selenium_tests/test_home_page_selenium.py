import allure


@allure.parent_suite("Selenium Framework")
@allure.suite("E-shop Tests")
def test_homepage_title(home_page_selenium, login_page_selenium):
    # 1. Otwieramy i logujemy się
    home_page_selenium.open_login_page()
    login_page_selenium.login_as_admin()

    # 2. Czekamy na załadowanie strony głównej po zalogowaniu
    home_page_selenium.wait_for_url(home_page_selenium.HOME_PAGE_URL)

    # 3. Sprawdzamy czy tytuł jest poprawny (zgodnie z nazwą testu)
    actual_title = home_page_selenium.get_title()
    expected_title = "Home Page - Web"
    assert expected_title in actual_title, f"Błąd! Oczekiwano '{expected_title}', a otrzymano '{actual_title}'"