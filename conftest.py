"""
Root conftest: register CLI options early so they work for any test path
(e.g. ``pytest selenium_tests/ --headless true``). Nested conftest
``pytest_addoption`` hooks can be registered too late for argument parsing.
"""


def pytest_addoption(parser):
    parser.addoption(
        "--remote",
        action="store",
        default="false",
        help="Selenium: use Remote WebDriver (Docker grid). true or false",
    )
    parser.addoption(
        "--headless",
        action="store",
        default="false",
        help="Selenium: run Chrome headless (new). true or false",
    )
