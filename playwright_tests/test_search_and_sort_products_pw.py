import allure


@allure.parent_suite("Playwright Framework")
@allure.suite("E-shop Tests")
def test_search_product_exists_pw(home_page_pw, login_page_pw, product_page_pw):
    print("\n[STEP] Open login page and sign in as admin.")
    home_page_pw.open_login_page_pw()
    login_page_pw.login_as_admin_pw()

    print("[STEP] Open bikes landing page and validate visible categories.")
    product_page_pw.open_bikes_main_link_pw()
    product_page_pw.assert_expected_bike_categories_pw()

    print("[STEP] Open Mountain Bikes subcategory.")
    product_page_pw.open_mountain_bikes_pw()

    print("[STEP] Validate All/Discounted filter consistency.")
    product_page_pw.assert_filter_counts_consistent_pw()

    print("[STEP] Validate all sorting options.")
    product_page_pw.all_sorting_options_pw()
    print("[DONE] Playwright search/sort scenario completed.")