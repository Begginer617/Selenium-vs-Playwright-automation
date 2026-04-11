import allure


@allure.parent_suite("Selenium Framework")
@allure.suite("E-shop Tests")
def test_multiple_products_total_calculation(home_page_selenium, login_page_selenium, product_page_selenium):
    # 1. Przygotowanie
    home_page_selenium.open_login_page()
    login_page_selenium.login_as_admin()

    # 2. Czyszczenie
    product_page_selenium.clear_cart()

    # 3. Wejście w kategorię
    product_page_selenium.open_mountain_bikes()

    # 4. Wielkie liczenie
    product_page_selenium.add_multiple_products_and_verify_total(count=5)