import allure


@allure.parent_suite("Selenium Framework")
@allure.suite("E-shop Tests")
def test_search_product_exists(home_page_selenium, login_page_selenium, product_page_selenium):
    # 1. Logowanie
    home_page_selenium.open_login_page()
    login_page_selenium.login_as_admin()

    # 2. Sprawdzenie kategorii na głównej stronie rowerów
    product_page_selenium.open_bikes_main_link()
    print("\n--- Sprawdzam kategorie na stronie głównej rowerów ---")

    titles = product_page_selenium.get_bike_category_titles()
    for t in titles:
        print(f"• {t}")

    assert "Mountain Bikes" in titles
    assert "Road Bikes" in titles
    assert "Touring Bikes" in titles

    # 3. Wejście w konkretną kategorię
    product_page_selenium.open_mountain_bikes()
    product_page_selenium.wait_for_page_load(2)

    # 4. Upewnij się, że zaznaczony jest filtr "All" (oczekujemy 32)
    product_page_selenium.click(product_page_selenium.ALL_BIKES_FILTER)
    product_page_selenium.wait_for_page_load(2)

    actual_count = product_page_selenium.get_total_count_from_pager()
    print(f"Liczba wszystkich produktów: {actual_count}")
    assert actual_count == 32, f"Expected 32 bikes, but found {actual_count}"

    # 5. Kliknij filtr Discounted i sprawdź wyniki (oczekujemy 8)
    product_page_selenium.click(product_page_selenium.DISCOUNTED_BIKES_FILTER)
    product_page_selenium.wait_for_page_load(2)

    actual_discounted_pager = product_page_selenium.get_total_count_from_pager()
    actual_badges = product_page_selenium.count_badges()
    visible_cards = product_page_selenium.count_visible_bikes()

    print(f"Pager: {actual_discounted_pager}, Plakietki: {actual_badges}, Karty: {visible_cards}")

    # 6. Asercje końcowe dla filtrów
    assert actual_discounted_pager == 8, f"Pager powinien pokazać 8, a pokazuje {actual_discounted_pager}"
    assert actual_badges == 8, "Liczba plakietek rabatowych powinna wynosić 8"
    assert visible_cards == 8, "Liczba widocznych kart powinna wynosić 8"

    print("\n✅ TEST ZAKOŃCZONY SUKCESEM!")

    # 7. Testowanie wszystkich opcji sortowania
    print("\n--- Rozpoczynam testy sortowania ---")
    product_page_selenium.all_sorting_options()