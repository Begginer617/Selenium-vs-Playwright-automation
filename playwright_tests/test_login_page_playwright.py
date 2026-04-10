import allure


@allure.parent_suite("Playwright Framework")
@allure.suite("E-shop Tests")
def test_login_flow_pw(home_page_pw, login_page_pw):
    home_page_pw.open_login_page_pw()
    login_page_pw.login_as_admin_pw()
    assert home_page_pw.is_logout_button_displayed()
    home_page_pw.click_logout_button()