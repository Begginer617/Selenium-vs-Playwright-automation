# playwright_tests/test_home_page_playwright.py
import allure


@allure.parent_suite("Playwright Framework")
@allure.suite("E-shop Tests")
def test_home_page_playwright(home_page_pw): # <--- Wstrzykujemy fixturę z conftest.py
    home_page_pw.open_home_page_pw()
    assert "Login" in home_page_pw.get_title()