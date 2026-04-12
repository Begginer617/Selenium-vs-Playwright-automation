import allure

@allure.parent_suite("Playwright Framework")
@allure.suite("E-shop Tests")
def test_registration_form_validation_pw(page, registration_page_pw):
    # 1. Wejdź na stronę
    registration_page_pw.open_registration_url_pw()

    # --- ETAP 1: TEST PUSTEGO FORMULARZA ---
    registration_page_pw.trigger_required_errors_pw()

    # Asercje dla Góry (Summary) - Playwright czeka automatycznie
    assert registration_page_pw.is_visible_pw(registration_page_pw.EMPTY_FIRST_AND_LAST_NAME_VALIDATION_SUMMARY_LIST)
    assert registration_page_pw.is_visible_pw(registration_page_pw.EMPTY_EMAIL_ERROR_VALIDATION_SUMMARY_LIST)
    assert registration_page_pw.is_visible_pw(registration_page_pw.EMPTY_PASSWORD_ERROR_VALIDATION_SUMMARY_LIST)

    # Asercje dla Dołu (Pod inputami)
    assert registration_page_pw.is_visible_pw(registration_page_pw.EMPTY_FIRST_AND_LAST_NAME_BOTTOM)
    assert "Email is required" in registration_page_pw.get_text_pw(registration_page_pw.EMPTY_EMAIL_ERROR_BOTTOM)
    assert "Please enter password" in registration_page_pw.get_text_pw(registration_page_pw.EMPTY_PASSWORD_ERROR_BOTTOM)

    # --- ETAP 2: TEST BŁĘDNEGO FORMATU ---
    page.reload() # Odpowiednik driver.refresh()

    registration_page_pw.trigger_format_errors_pw(
        incorrect_name="Tester",
        incorrect_email="zly_email.pl",
        short_password="123"
    )

    # Asercje dla Góry
    assert registration_page_pw.is_visible_pw(registration_page_pw.FIRST_AND_LAST_NAME_SEPARATED_BY_A_SPACE_VALIDATION_SUMMARY_LIST)
    assert registration_page_pw.is_visible_pw(registration_page_pw.EMAIL_IS_NOT_VALID_VALIDATION_SUMMARY_LIST)
    assert registration_page_pw.is_visible_pw(registration_page_pw.PASSWORD_REQUIREMENTS_VALIDATION_SUMMARY_LIST)

    # Asercje dla Dołu
    assert "separated by a space" in registration_page_pw.get_text_pw(registration_page_pw.FIRST_AND_LAST_NAME_SEPARATED_BY_A_SPACE_BOTTOM)
    assert "not valid email" in registration_page_pw.get_text_pw(registration_page_pw.EMAIL_IS_NOT_VALID_EMAIL_BOTTOM)
    assert "8 symbols" in registration_page_pw.get_text_pw(registration_page_pw.PASSWORD_REQUIREMENTS_BOTTOM)

    print("✅ Sukces: Wszystkie 12 punktów walidacji sprawdzonych!")