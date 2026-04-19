import allure

@allure.parent_suite("Playwright Framework")
@allure.suite("E-shop Tests")
def test_header_page_playwright(home_page_pw, login_page_pw, header_page_pw):
    print("\n[STEP] Open login page and sign in.")
    home_page_pw.open_login_page_pw()
    login_page_pw.login_as_admin_pw()

    print("[STEP] Validate header routes via page object helper.")
    header_page_pw.validate_header_navigation_pw()
    print("[DONE] Header navigation checks completed.")