import allure

@allure.parent_suite("Playwright Framework")
@allure.suite("E-shop Tests")
def test_adding_multiple_items_to_basket_playwright_pw(home_page_pw, login_page_pw, product_page_pw):
    print("\n[STEP] Logging in as admin user.")
    home_page_pw.open_login_page_pw()
    login_page_pw.login_as_admin_pw()

    print("[STEP] Clearing the shopping cart.")
    product_page_pw.clear_cart_pw()

    print("[STEP] Navigating to products page.")
    product_page_pw.open_bikes_main_link_pw()
    print("[STEP] Opening Mountain Bikes category.")
    product_page_pw.open_mountain_bikes_pw()

    print("[STEP] Adding multiple products and validating total.")
    product_page_pw.add_multiple_products_and_verify_total_pw(count=5)
    print("[DONE] Multiple products total calculation flow finished successfully.")