def test_header_page_selenium(home_page_selenium, login_page, header_page_selenium):
    # 1. Otwórz stronę logowania
    home_page_selenium.open_login_page()

    # 2. Zaloguj się (używamy fixtury login_page)
    login_page.login_as_admin()

    # 3. Kliknij w koszyk używając Twojej metody z klasy HeaderSeleniumPage
    # Używamy nazwy fixtury: header_page_selenium
    header_page_selenium.click_cart()

    # Opcjonalnie: sprawdź czy jesteś w koszyku
    assert "ShoppingCart" in header_page_selenium.driver.current_url

    # 4. POWRÓT NA STRONĘ GŁÓWNĄ (To jest kluczowe!)
    # Zamiast home_page_selenium.open_login_page(), używamy bezpośredniego przejścia:
    header_page_selenium.driver.get("https://demos.telerik.com/kendo-ui/eshop")

    # Opcjonalnie: upewnij się, że strona się załadowała
    assert "https://demos.telerik.com/kendo-ui/eshop" in header_page_selenium.driver.current_url

    # 5. TERAZ HOVER I KLIKNIĘCIE
    # Skoro jesteś na właściwej stronie, menu "Categories" powinno być widoczne i działać
    header_page_selenium.open_accessories_category()

    # 6. Finalna asercja
    assert "Home/Accessories" in header_page_selenium.driver.current_url


