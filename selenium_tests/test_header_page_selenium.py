import allure


@allure.parent_suite("Selenium Framework")
@allure.suite("E-shop Tests")
def test_header_page_selenium(home_page_selenium, login_page_selenium, header_page_selenium):
    # 1. Open login page and sign in.
    home_page_selenium.open_login_page()
    login_page_selenium.login_as_admin()
    # 2. Validate all header navigation paths.
    header_page_selenium.validate_header_navigation()