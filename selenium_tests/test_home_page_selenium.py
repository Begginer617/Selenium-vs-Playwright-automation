def test_homepage_title(home_page_selenium, login_page_selenium):
    # 1. Otwieramy i logujemy się
    home_page_selenium.open_login_page()
    login_page_selenium.login_as_admin()

    # 2. Czekamy na URL (teraz bez slasha w zmiennej przejdzie od razu!)
    home_page_selenium.wait_for_url(home_page_selenium.HOME_PAGE_URL)

    # 3. Sprawdzamy tytuł lub URL
    assert home_page_selenium.HOME_PAGE_URL in login_page_selenium.driver.current_url