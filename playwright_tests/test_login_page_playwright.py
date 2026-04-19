import allure
from playwright.sync_api import expect


@allure.parent_suite("Playwright Framework")
@allure.suite("E-shop Tests")
def test_login_flow_pw(home_page_pw, login_page_pw):
    print("[STEP] Open login page")
    home_page_pw.open_login_page_pw()
    print("[STEP] Login as admin")
    login_page_pw.login_as_admin_pw()
    print("[ASSERT] Verify authenticated favorites link is visible")
    expect(login_page_pw.page.locator(login_page_pw.AUTHENTICATED_FAVORITES_LINK).first).to_be_visible()
    print("[STEP] Logout")
    home_page_pw.click_logout_button_pw()
    print("[DONE] test_login_flow_pw completed")