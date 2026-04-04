from selenium.webdriver.support.wait import WebDriverWait


def test_search_product_exists(home_page_selenium, login_page_selenium, product_page_selenium):
    # 1. Logowanie
    home_page_selenium.open_login_page()
    login_page_selenium.login_as_admin()

    # 2. Nawigacja do rowerów górskich
    product_page_selenium.open_bikes_main_link()
    product_page_selenium.open_mountain_bikes()

    # 3. Upewnij się, że zaznaczony jest filtr "All"
    # Używamy metody click z BasePage, podając jej lokator
    product_page_selenium.click(product_page_selenium.ALL_BIKES_FILTER)
    product_page_selenium.wait_for_page_load(2)

    # 4. Pobierz faktyczną liczbę z pagera
    actual_count = product_page_selenium.get_total_count_from_pager()

    # 5. Asercja i raportowanie
    expected_count = 32

    if actual_count != expected_count:
        print(f" Incorrect number of products found: {actual_count}")
    else:
        print(f" Correct number of products found: {actual_count}")

    assert actual_count == expected_count, f"Expected {expected_count} bikes, but found {actual_count}"


    #6.kliknij button discounted o sprawdź ile jest produktów





    #7.
    #8. sprawdz czy wsztkie maja labele z obizka ceny
    #9. wejdz na jedn z produktow i sprawdz czy w adresie url product id zgadza sie z tym co jest na stronie wystetlone ( nie wiem czy taki test ma sens)


    titles = product_page_selenium.get_bike_category_titles()

    print("\n--- Kategorie znalezione przez Selenium ---")
    for t in titles:
        print(f"• {t}")

    print("\n--- Sprawdzam asercje ---")
    print("Czy jest Mountain Bikes:", "Mountain Bikes" in titles)
    print("Czy jest Road Bikes:", "Road Bikes" in titles)
    print("Czy jest Touring Bikes:", "Touring Bikes" in titles)

    assert "Mountain Bikes" in titles
    assert "Road Bikes" in titles
    assert "Touring Bikes" in titles



def test_sort_options(home_page_selenium, login_page_selenium, products_page_selenium):
    home_page_selenium.HOME_PAGE_URL()




    # Sorotwanie TC
    # 1.Wybierz categorie bikes
    # 2. Mountain Bikes wybierz
    # 3. wybierz Price - High to Low and check if sorting works
    # 4. wybierz Price - Low to High check if sorting works
    # 5. wybierz Price - Name - A to Z check if sorting works
    # 5. wybierz Price - Name - z to a check if sorting works

    # Sprawdzanie czy produkt istnieje TC
    # 1.Wybierz categories bikes i co w nie jest

    #Sprawdzenie filtrow obecnie 32 produktow
    #Discount -  czy wyświetla produktu discount
    #Size -  czy lista wyników sie zmienia pod wpływem filtru, zaznacz 1 i zaznacz wszystkie
    #Model -  czy lista wyników sie zmienia pod wpływem filtru
    #Color -  czy lista wyników sie zmienia pod wpływem filtru
    #Rating -  czy lista wyników sie zmienia pod wpływem filtru
    # Clear All - czy czysci filtry ( na samym koncu )