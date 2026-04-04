from selenium.webdriver.support.wait import WebDriverWait


def test_search_product_exists(home_page_selenium, login_page_selenium, product_page_selenium):
    home_page_selenium.open_login_page()
    login_page_selenium.login_as_admin()

    product_page_selenium.open_bikes_main_link()

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