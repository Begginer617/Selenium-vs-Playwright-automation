import allure


@allure.parent_suite("Playwright Framework")
@allure.suite("E-shop Tests")
def test_add_to_cart_flow_pw(home_page_pw, login_page_pw, products_page_pw):
    home_page_pw.open_login_page_pw()
    login_page_pw.login_as_admin_pw()

    # WYCZYŚĆ KOSZYK
    products_page_pw.clear_cart_pw()

    # DODAJ JEDEN
    products_page_pw.open_main_pw()
    products_page_pw.open_mountain_bikes_pw()
    products_page_pw.add_first_product_pw()
