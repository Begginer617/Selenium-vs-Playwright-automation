import allure
import pytest


@allure.parent_suite("Selenium Framework")
@allure.suite("E-shop Tests")
@pytest.mark.parametrize("scenario_name", ["required", "invalid_format"])
def test_registration_form_validation(driver, registration_page_selenium, scenario_name):
    print(f"\n[STEP][Selenium][Registration] Start scenario: {scenario_name}")
    registration_page_selenium.open_registration_url()

    if scenario_name == "required":
        print("[STEP] Trigger required-field validation errors")
        registration_page_selenium.trigger_required_errors()
        print("[ASSERT] Validate required-field error messages")
        registration_page_selenium.assert_required_errors()
    else:
        print("[STEP] Refresh page before invalid-format scenario")
        driver.refresh()
        print("[STEP] Trigger invalid-format validation errors")
        registration_page_selenium.trigger_format_errors(
            incorrect_name="Tester",
            incorrect_email="zly_email.pl",
            short_password="123",
        )
        print("[ASSERT] Validate invalid-format error messages")
        registration_page_selenium.assert_format_errors()
    print(f"[DONE][Selenium][Registration] Scenario passed: {scenario_name}")



