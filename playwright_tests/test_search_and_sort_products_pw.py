import allure
import pytest

@allure.parent_suite("Playwright Framework")
@allure.suite("E-shop Tests")
def test_search_product_exists_pw(home_page_pw, login_page_pw, product_page_pw):
    # 1. Logowanie
    home_page_pw.open_login_page_pw()
    login_page_pw.login_as_admin_pw()

    # 2. Sprawdzenie kategorii na głównej stronie rowerów
    product_page_pw.open_bikes_main_link_pw()
    print("\n--- Sprawdzam kategorie na stronie głównej rowerów ---")

    titles = product_page_pw.get_bike_category_titles_pw()
    for t in titles:
        print(f"• {t}")

    assert "Mountain Bikes" in titles
    assert "Road Bikes" in titles
    assert "Touring Bikes" in titles

    # 3. Wejście w konkretną kategorię
    product_page_pw.open_mountain_bikes_pw()

    # 4. Upewnij się, że zaznaczony jest filtr "All" (oczekujemy 32)
    product_page_pw.click_filter_all_pw()

    actual_count = product_page_pw.get_total_count_from_pager_pw()
    print(f"Liczba wszystkich produktów: {actual_count}")
    assert actual_count == 32, f"Expected 32 bikes, but found {actual_count}"

    # 5. Kliknij filtr Discounted i sprawdź wyniki (oczekujemy 8)
    product_page_pw.click_filter_discounted_pw()
    product_page_pw.debug_page_content_pw()

    actual_discounted_pager = product_page_pw.get_total_count_from_pager_pw()
    actual_badges = product_page_pw.count_badges_pw()
    visible_cards = product_page_pw.count_visible_bikes_pw()

    print(f"Pager: {actual_discounted_pager}, Plakietki: {actual_badges}, Karty: {visible_cards}")

    # 6. Asercje końcowe dla filtrów
    assert actual_discounted_pager == 8, f"Pager powinien pokazać 8, a pokazuje {actual_discounted_pager}"
    assert actual_badges == 8, "Liczba plakietek rabatowych powinna wynosić 8"
    assert visible_cards == 8, "Liczba widocznych kart powinna wynosić 8"

    print("\n✅ TEST ZAKOŃCZONY SUKCESEM!")

    # 7. Testowanie wszystkich opcji sortowania
    print("\n--- Rozpoczynam testy sortowania ---")
    product_page_pw.all_sorting_options_pw()