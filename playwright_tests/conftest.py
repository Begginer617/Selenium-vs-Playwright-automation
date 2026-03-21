import pytest

@pytest.fixture
def page(playwright_browser_context):
    # Setup specyficzny dla Playwrighta
    page = playwright_browser_context.new_page()
    yield page
    # Playwright sam sprząta po sobie lepiej niż Selenium,
    # ale tutaj możesz dodać np. zamykanie nagranych filmów z testu.
    page.close()