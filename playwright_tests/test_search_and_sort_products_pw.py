import allure


@allure.parent_suite("Playwright Framework")
@allure.suite("E-shop Tests")
def test_search_product_exists_pw(home_page_pw, login_page_pw, product_page_pw):
    # 1. Login
    home_page_pw.open_login_page_pw()
    login_page_pw.login_as_admin_pw()

    # 2. Validate bike categories
    product_page_pw.open_bikes_main_link_pw()
    product_page_pw.assert_expected_bike_categories_pw()

    # 3. Enter mountain bikes category
    product_page_pw.open_mountain_bikes_pw()

    # 4. Validate filters with dynamic checks
    product_page_pw.assert_filter_counts_consistent_pw()

    # 5. Validate all sorting options
    product_page_pw.all_sorting_options_pw()