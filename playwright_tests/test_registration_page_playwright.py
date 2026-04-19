import allure
import pytest

@allure.parent_suite("Playwright Framework")
@allure.suite("E-shop Tests")
@pytest.mark.parametrize("scenario_name", ["required", "invalid_format"])
def test_registration_form_validation_pw(page, registration_page_pw, scenario_name):
    registration_page_pw.open_registration_url_pw()

    if scenario_name == "required":
        registration_page_pw.trigger_required_errors_pw()
        registration_page_pw.expect_required_errors_pw()
    else:
        page.reload()
        registration_page_pw.trigger_format_errors_pw(
            incorrect_name="Tester",
            incorrect_email="zly_email.pl",
            short_password="123",
        )
        registration_page_pw.expect_format_errors_pw()