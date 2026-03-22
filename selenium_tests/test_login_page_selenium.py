import pytest
from pages.selenium.login_page_selenium import LoginPage


@pytest.fixture
def login_page(driver):
    return LoginPage(driver)


def test_registration_form_validation(driver, login_page):
    # 1. Wejdź na stronę
    driver.get("https://demos.telerik.com/kendo-ui/eshop/Account/Register")

    # --- ETAP 1: TEST PUSTEGO FORMULARZA ---
    # Klikamy register bez wpisywania czegokolwiek
    login_page.trigger_required_errors()

    # Asercje dla Góry (Summary)
    assert login_page.wait_for_visible(login_page.EMPTY_FIRST_AND_LAST_NAME_VALIDATION_SUMMARY_LIST).is_displayed()
    assert login_page.wait_for_visible(login_page.EMPTY_EMAIL_ERROR_VALIDATION_SUMMARY_LIST).is_displayed()
    assert login_page.wait_for_visible(login_page.EMPTY_PASSWORD_ERROR_VALIDATION_SUMMARY_LIST).is_displayed()

    # Asercje dla Dołu (Pod inputami)
    assert login_page.wait_for_visible(login_page.EMPTY_FIRST_AND_LAST_NAME_BOTTOM).is_displayed()
    assert "Email is required" in login_page.wait_for_visible(login_page.EMPTY_EMAIL_ERROR_BOTTOM).text
    assert "Please enter password" in login_page.wait_for_visible(login_page.EMPTY_PASSWORD_ERROR_BOTTOM).text

    # --- ETAP 2: TEST BŁĘDNEGO FORMATU ---
    # Odświeżamy stronę, żeby wyczyścić stan
    driver.refresh()

    login_page.trigger_format_errors(
        incorrect_name="Tester",
        incorrect_email="zly_email.pl",
        short_password="123"
    )

    # Asercje dla Góry
    assert login_page.wait_for_visible(
        login_page.FIRST_AND_LAST_NAME_SEPARATED_BY_A_SPACE_VALIDATION_SUMMARY_LIST).is_displayed()
    assert login_page.wait_for_visible(login_page.EMAIL_IS_NOT_VALID_VALIDATION_SUMMARY_LIST).is_displayed()
    assert login_page.wait_for_visible(login_page.PASSWORD_REQUIREMENTS_VALIDATION_SUMMARY_LIST).is_displayed()

    # Asercje dla Dołu
    assert "separated by a space" in login_page.wait_for_visible(
        login_page.FIRST_AND_LAST_NAME_SEPARATED_BY_A_SPACE_BOTTOM).text
    assert "not valid email" in login_page.wait_for_visible(login_page.EMAIL_IS_NOT_VALID_EMAIL_BOTTOM).text
    assert "8 symbols" in login_page.wait_for_visible(login_page.PASSWORD_REQUIREMENTS_BOTTOM).text

    print("✅ Sukces: Wszystkie 12 punktów walidacji sprawdzonych!")
