import allure
import pytest


@allure.parent_suite("Selenium Framework")
@allure.suite("E-shop Tests")
@pytest.mark.parametrize("scenario_name", ["required", "invalid_format"])
def test_registration_form_validation(driver, registration_page_selenium, scenario_name):
    registration_page_selenium.open_registration_url()

    if scenario_name == "required":
        registration_page_selenium.trigger_required_errors()
        registration_page_selenium.assert_required_errors()
    else:
        driver.refresh()
        registration_page_selenium.trigger_format_errors(
            incorrect_name="Tester",
            incorrect_email="zly_email.pl",
            short_password="123",
        )
        registration_page_selenium.assert_format_errors()



