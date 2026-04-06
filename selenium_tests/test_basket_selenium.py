def test_add_to_cart_flow(home_page_selenium, login_page_selenium, product_page_selenium):
    home_page_selenium.open_login_page()
    login_page_selenium.login_as_admin()

    # WYCZYŚĆ KOSZYK
    product_page_selenium.clear_cart()

    # DODAJ JEDEN
    product_page_selenium.open_mountain_bikes()
    product_page_selenium.add_first_product_to_cart_and_verify()