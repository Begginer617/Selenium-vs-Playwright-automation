def test_login_flow(home_page_selenium, login_page_selenium):
    # 1. Wejdź na stronę logowania
    home_page_selenium.open_login_page()

    # 2. Zaloguj się (używając nowej, czystej metody z LoginPage)
    login_page_selenium.login_as_admin()