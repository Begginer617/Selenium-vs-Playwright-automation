
import allure



@allure.parent_suite("Selenium Framework")
@allure.suite("E-shop Tests")
def test_registration_form_validation(driver, registration_page):
    # 1. Wejdź na stronę
    # driver.get("https://demos.telerik.com/kendo-ui/eshop/Account/Register")
    registration_page.open_registration_url()


    # --- ETAP 1: TEST PUSTEGO FORMULARZA ---
    # Klikamy register bez wpisywania czegokolwiek
    registration_page.trigger_required_errors()

    # Asercje dla Góry (Summary)
    assert registration_page.wait_for_visible(registration_page.EMPTY_FIRST_AND_LAST_NAME_VALIDATION_SUMMARY_LIST).is_displayed()
    assert registration_page.wait_for_visible(registration_page.EMPTY_EMAIL_ERROR_VALIDATION_SUMMARY_LIST).is_displayed()
    assert registration_page.wait_for_visible(registration_page.EMPTY_PASSWORD_ERROR_VALIDATION_SUMMARY_LIST).is_displayed()

    # Asercje dla Dołu (Pod inputami)
    assert registration_page.wait_for_visible(registration_page.EMPTY_FIRST_AND_LAST_NAME_BOTTOM).is_displayed()
    assert "Email is required" in registration_page.wait_for_visible(registration_page.EMPTY_EMAIL_ERROR_BOTTOM).text
    assert "Please enter password" in registration_page.wait_for_visible(registration_page.EMPTY_PASSWORD_ERROR_BOTTOM).text

    # --- ETAP 2: TEST BŁĘDNEGO FORMATU ---
    # Odświeżamy stronę, żeby wyczyścić stan
    driver.refresh()

    registration_page.trigger_format_errors(
        incorrect_name="Tester",
        incorrect_email="zly_email.pl",
        short_password="123"
    )

    # Asercje dla Góry
    assert registration_page.wait_for_visible(
        registration_page.FIRST_AND_LAST_NAME_SEPARATED_BY_A_SPACE_VALIDATION_SUMMARY_LIST).is_displayed()
    assert registration_page.wait_for_visible(registration_page.EMAIL_IS_NOT_VALID_VALIDATION_SUMMARY_LIST).is_displayed()
    assert registration_page.wait_for_visible(registration_page.PASSWORD_REQUIREMENTS_VALIDATION_SUMMARY_LIST).is_displayed()

    # Asercje dla Dołu
    assert "separated by a space" in registration_page.wait_for_visible(
        registration_page.FIRST_AND_LAST_NAME_SEPARATED_BY_A_SPACE_BOTTOM).text
    assert "not valid email" in registration_page.wait_for_visible(registration_page.EMAIL_IS_NOT_VALID_EMAIL_BOTTOM).text
    assert "8 symbols" in registration_page.wait_for_visible(registration_page.PASSWORD_REQUIREMENTS_BOTTOM).text

    print("✅ Sukces: Wszystkie 12 punktów walidacji sprawdzonych!")



