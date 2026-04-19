import allure


@allure.parent_suite("Selenium Framework")
@allure.suite("E-shop Tests")
def test_header_page_selenium(home_page_selenium, login_page_selenium, header_page_selenium):
    print("[STEP] Open login page.")
    # 1. Open login page and sign in.
    home_page_selenium.open_login_page()
    print("[STEP] Login as admin user.")
    login_page_selenium.login_as_admin()
    print("[STEP] Validate header navigation routes.")
    # 2. Validate all header navigation paths.
    header_page_selenium.validate_header_navigation()
    print("[DONE] Header navigation validation completed.")