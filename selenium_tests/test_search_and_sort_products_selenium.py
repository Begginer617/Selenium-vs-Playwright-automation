import allure


@allure.parent_suite("Selenium Framework")
@allure.suite("E-shop Tests")
def test_search_product_exists(home_page_selenium, login_page_selenium, product_page_selenium):
    # 1. Login
    home_page_selenium.open_login_page()
    login_page_selenium.login_as_admin()

    # 2. Validate category visibility on bikes landing page.
    product_page_selenium.open_bikes_main_link()
    product_page_selenium.assert_expected_bike_categories(
        ["Mountain Bikes", "Road Bikes", "Touring Bikes"]
    )

    # 3. Enter specific category.
    product_page_selenium.open_mountain_bikes()
    product_page_selenium.wait_for_page_load(2)

    # 4. Validate All + Discounted filters with dynamic consistency checks.
    product_page_selenium.assert_filter_counts_consistent()

    # 6. Validate sorting options.
    product_page_selenium.all_sorting_options()