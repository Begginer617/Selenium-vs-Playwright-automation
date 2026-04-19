import allure


@allure.parent_suite("Selenium Framework")
@allure.suite("E-shop Tests")
def test_multiple_products_total_calculation(home_page_selenium, login_page_selenium, product_page_selenium):
    print("[STEP] Open login page and authenticate.")
    home_page_selenium.open_login_page()
    login_page_selenium.login_as_admin()

    print("[STEP] Clear cart before multi-product total verification.")
    product_page_selenium.clear_cart()

    print("[STEP] Open mountain bikes category.")
    product_page_selenium.open_mountain_bikes()

    print("[STEP] Add multiple products and validate computed cart total.")
    product_page_selenium.add_multiple_products_and_verify_total(count=3)
    print("[DONE] Multi-product total calculation flow completed.")