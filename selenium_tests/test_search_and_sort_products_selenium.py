import allure


@allure.parent_suite("Selenium Framework")
@allure.suite("E-shop Tests")
def test_search_product_exists(home_page_selenium, login_page_selenium, product_page_selenium):
    print("\n[STEP] Open login page and authenticate.")
    home_page_selenium.open_login_page()
    login_page_selenium.login_as_admin()

    print("[STEP] Open bikes landing page and validate category blocks.")
    product_page_selenium.open_bikes_main_link()
    product_page_selenium.assert_expected_bike_categories(
        ["Mountain Bikes", "Road Bikes", "Touring Bikes"]
    )

    print("[STEP] Open mountain bikes category.")
    product_page_selenium.open_mountain_bikes()
    product_page_selenium.wait_for_page_load(2)

    print("[ASSERT] Validate All and Discounted filter consistency.")
    product_page_selenium.assert_filter_counts_consistent()

    print("[ASSERT] Validate all sorting options.")
    product_page_selenium.all_sorting_options()
    print("[DONE] Search and sort flow completed.")