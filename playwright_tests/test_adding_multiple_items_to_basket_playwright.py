import allure

@allure.parent_suite("Playwright Framework")
@allure.suite("E-shop Tests")
def test_adding_multiple_items_to_basket_playwright_pw(home_page_pw, login_page_pw, products_page_pw):
    print("\n[STEP] Logowanie...")
    home_page_pw.open_login_page_pw()
    login_page_pw.login_as_admin_pw()

    print("[STEP] Czyszczenie koszyka...")
    products_page_pw.clear_cart_pw()

    # WAŻNE: Musisz przejść do strony z produktami!
    print("[STEP] Przechodzę do strony produktów...")
    products_page_pw.open_main_pw()

    products_page_pw.open_mountain_bikes_pw()

    print("[STEP] Dodawanie wielu produktów...")
    products_page_pw.add_multiple_products_and_verify_total_pw(count=5)