def test_header_page_selenium(home_page_selenium, login_page, header_page_selenium):
    # 1. Otwórz stronę logowania i zaloguj się
    home_page_selenium.open_login_page()
    login_page.login_as_admin()

    # 2. Test Koszyka
    header_page_selenium.click_cart()
    assert "ShoppingCart" in header_page_selenium.get_url()
    # 3. Powrót na główną przed testem kategorii
    header_page_selenium.open_home_page()
    assert "ShoppingCart" in header_page_selenium.get_url()
    # 4. Test Accessories
    header_page_selenium.open_accessories_category()
    assert "ShoppingCart" in header_page_selenium.get_url()
    # 5. Test Bikes
    header_page_selenium.open_home_page()
    header_page_selenium.open_bikes_category()
    assert "ShoppingCart" in header_page_selenium.get_url()
    # 6. Test Clothes (URL to /Home/Clothing)
    header_page_selenium.open_home_page()
    header_page_selenium.open_clothes_category()
    assert "ShoppingCart" in header_page_selenium.get_url()
    # 7. Test Components
    header_page_selenium.open_home_page()
    header_page_selenium.open_components_category()
    assert "ShoppingCart" in header_page_selenium.get_url()
