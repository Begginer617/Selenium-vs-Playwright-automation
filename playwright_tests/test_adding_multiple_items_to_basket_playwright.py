import allure
import pytest


@allure.parent_suite("Playwright Framework")
@allure.suite("E-shop Tests")
@pytest.mark.flaky(reruns=2, reruns_delay=2)
def test_multiple_products_total_calculation_pw(home_page_pw, login_page_pw, product_page_pw):
    print("[STEP] Open login page and authenticate.")
    # DODAJ _pw NA KOŃCU:
    home_page_pw.open_login_page_pw()
    login_page_pw.login_as_admin_pw()

    print("[STEP] Navigate to Bikes and clear cart.")
    product_page_pw.page.goto(product_page_pw.BIKE_MAIN_LINK)
    product_page_pw.clear_cart_pw()

    print("[STEP] Open mountain bikes category.")
    product_page_pw.open_mountain_bikes_pw()


    print("[STEP] Add multiple products and validate computed cart total.")
    product_page_pw.add_multiple_products_and_verify_total_pw(count=5)


