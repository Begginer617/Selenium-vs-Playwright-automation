import allure


@allure.parent_suite("Selenium Framework")
@allure.suite("E-shop Tests")
def test_login_flow(home_page_selenium, login_page_selenium):
    # 1. Open the login page.
    home_page_selenium.open_home_page()
    home_page_selenium.open_login_page()
    # 2. Log in as admin and verify post-login state.
    login_page_selenium.login_as_admin()
    current_url = home_page_selenium.driver.current_url
    assert "Account/Login" not in current_url, (
        f"Expected not to remain on login page after auth, got URL: {current_url}"
    )
    assert "eshop" in current_url, f"Expected to be inside e-shop after login, got URL: {current_url}"