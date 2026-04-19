import allure


@allure.parent_suite("Selenium Framework")
@allure.suite("E-shop Tests")
def test_homepage_title(home_page_selenium, login_page_selenium):
    print("\n[STEP] Open login page and authenticate user")
    home_page_selenium.open_login_page()
    login_page_selenium.login_as_admin()

    print("[STEP] Wait for home page URL after login")
    home_page_selenium.wait_for_url(home_page_selenium.HOME_PAGE_URL)

    print("[ASSERT] Validate home page title")
    actual_title = home_page_selenium.get_title()
    expected_title = "Home Page - Web"
    assert expected_title in actual_title, (
        f"Expected title containing '{expected_title}', got '{actual_title}'"
    )
    print("[DONE] Home page title test passed")