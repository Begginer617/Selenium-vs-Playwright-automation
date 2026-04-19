import allure


@allure.parent_suite("Selenium Framework")
@allure.suite("E-shop Tests")
def test_add_to_cart_flow(home_page_selenium, login_page_selenium, product_page_selenium):
    print("\n[STEP][Selenium][Basket] Open login page and authenticate.")
    home_page_selenium.open_login_page()
    login_page_selenium.login_as_admin()

    print("[STEP][Selenium][Basket] Clear cart before scenario.")
    product_page_selenium.clear_cart()

    print("[STEP][Selenium][Basket] Open mountain bikes and add first product.")
    product_page_selenium.open_mountain_bikes()
    product_page_selenium.add_first_product_to_cart_and_verify()
    print("[DONE][Selenium][Basket] Add-to-cart flow completed.")