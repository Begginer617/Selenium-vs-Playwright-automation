import allure


@allure.parent_suite("Playwright Framework")
@allure.suite("E-shop Tests")
def test_home_page_playwright(home_page_pw):
    print("\n[STEP 1] Otwieram stronę główną...")
    home_page_pw.open_home_page_pw()

    print("[STEP 2] Sprawdzam tytuł strony...")
    title = home_page_pw.get_title()
    print(f"[DEBUG] Pobrano tytuł: '{title}'")

    assert "Login" in title
    print("✅ TEST PASSED: Tytuł zawiera 'Login'.")