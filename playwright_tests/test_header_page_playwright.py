import allure

@allure.parent_suite("Playwright Framework")
@allure.suite("E-shop Tests")
def test_header_page_playwright(home_page_pw, login_page_pw, header_page_pw):
    # 1. Otwórz stronę logowania i zaloguj się
    home_page_pw.open_login_page_pw()
    login_page_pw.login_as_admin_pw()

    # 2. Test Koszyka
    header_page_pw.click_cart_pw()
    assert "ShoppingCart" in header_page_pw.get_url_pw()

    # 3. Powrót na główną
    home_page_pw.open_home_page_pw()
    assert "eshop" in header_page_pw.get_url_pw()

    # 4. Test Accessories
    header_page_pw.open_accessories_category_pw()
    assert "Home/Accessories" in header_page_pw.get_url_pw()

    # 5. Test Bikes
    header_page_pw.open_home_page_pw()
    header_page_pw.open_bikes_category_pw()
    assert "Home/Bikes" in header_page_pw.get_url_pw()

    # 6. Test Clothes
    header_page_pw.open_home_page_pw()
    header_page_pw.open_clothes_category_pw()
    assert "Home/Clothing" in header_page_pw.get_url_pw()

    # 7. Test Components
    header_page_pw.open_home_page_pw()
    header_page_pw.open_components_category_pw()
    assert "Home/Components" in header_page_pw.get_url_pw()