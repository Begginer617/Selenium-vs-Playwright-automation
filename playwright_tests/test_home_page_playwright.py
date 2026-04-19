import allure


@allure.parent_suite("Playwright Framework")
@allure.suite("E-shop Tests")
def test_home_page_playwright(home_page_pw):
    print("\n[STEP] Open home page.")
    home_page_pw.open_home_page_pw()

    print("[STEP] Validate page title.")
    title = home_page_pw.get_title()
    print(f"[DEBUG] Retrieved title: '{title}'")

    print("[ASSERT] Title should contain 'Login'.")
    assert "Login" in title
    print("[DONE] Home page title validation passed.")