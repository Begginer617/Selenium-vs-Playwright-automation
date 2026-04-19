import allure


@allure.parent_suite("Playwright Framework")
@allure.suite("E-shop Tests")
def test_add_to_cart_flow_pw(home_page_pw, login_page_pw, product_page_pw):
    print("\n[PW][STEP] Open login page and sign in")
    home_page_pw.open_login_page_pw()
    login_page_pw.login_as_admin_pw()

    print("[PW][STEP] Clear cart before adding a product")
    product_page_pw.clear_cart_pw()

    print("[PW][STEP] Add one product and validate cart item")
    product_page_pw.open_bikes_main_link_pw()\
                    .open_mountain_bikes_pw()\
                    .add_first_product_to_cart_and_verify_pw()
    print("[PW][DONE] Basket flow completed")