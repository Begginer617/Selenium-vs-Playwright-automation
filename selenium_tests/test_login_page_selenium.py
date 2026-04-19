import allure


@allure.parent_suite("Selenium Framework")
@allure.suite("E-shop Tests")
def test_login_flow(home_page_selenium, login_page_selenium):
    # 1. Open the login page.
    home_page_selenium.open_home_page()
    home_page_selenium.open_login_page()
    # 2. Log in as admin and verify post-login state.
    login_page_selenium.login_as_admin()
    assert login_page_selenium.is_logged_in(), "Expected user to be logged in after admin login flow."