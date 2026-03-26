def test_header_page_selenium(home_page_selenium, login_page, header_page_selenium):
    # 1. Otwórz stronę logowania
    home_page_selenium.open_login_page()

    # 2. Zaloguj się (używamy fixtury login_page)
    login_page.login_as_admin()

    # 3. Kliknij w koszyk
    # Używamy nazwy fixtury: header_page_selenium
    header_page_selenium.click_cart()

    # Sprawdź czy jesteś w koszyku
    assert "ShoppingCart" in header_page_selenium.driver.current_url

    # 4. POWRÓT NA STRONĘ GŁÓWNĄ
    # Zamiast home_page_selenium.open_login_page(), używamy bezpośredniego przejścia:
    header_page_selenium.driver.get("https://demos.telerik.com/kendo-ui/eshop")
    assert "https://demos.telerik.com/kendo-ui/eshop" in header_page_selenium.driver.current_url

    # 5. Test Accessories
    header_page_selenium.open_accessories_category()
    assert "Home/Accessories" in header_page_selenium.driver.current_url
    header_page_selenium.driver.get("https://demos.telerik.com/kendo-ui/eshop")

    # 6. Test Bikes
    header_page_selenium.open_bikes_category()
    assert "Home/Bikes" in header_page_selenium.driver.current_url
    header_page_selenium.driver.get("https://demos.telerik.com/kendo-ui/eshop")

    # 7. Test Clothes (Pamiętaj o /Clothing w URL!)
    header_page_selenium.open_clothes_category()
    assert "Home/Clothing" in header_page_selenium.driver.current_url
    header_page_selenium.driver.get("https://demos.telerik.com/kendo-ui/eshop")

    # 8. Test Components
    header_page_selenium.open_components_category()
    assert "Home/Components" in header_page_selenium.driver.current_url







