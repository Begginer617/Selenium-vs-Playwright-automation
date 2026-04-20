import pytest
import allure

@allure.parent_suite("Selenium Framework")
@allure.suite("E-shop Tests")
@pytest.mark.flaky(reruns=2, reruns_delay=2)  # 2 reruns, 2s between attempts
def test_multiple_products_total_calculation(home_page_selenium, login_page_selenium, product_page_selenium):
    print("[STEP] Open login page and authenticate.")
    home_page_selenium.open_login_page()
    login_page_selenium.login_as_admin()

    print("[STEP] Clear cart before multi-product total verification.")
    # POM clear_cart() returns to the Bikes landing page when done
    product_page_selenium.clear_cart()

    print("[STEP] Open mountain bikes category.")
    product_page_selenium.open_mountain_bikes()

    print("[STEP] Add multiple products and validate computed cart total.")
    # count=3 keeps Selenium total-validation stable
    product_page_selenium.add_multiple_products_and_verify_total(count=3)
    print("[DONE] Multi-product total calculation flow completed.")