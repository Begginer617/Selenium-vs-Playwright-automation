import time

from pages.selenium.home_page_selenium import HomePage

def test_homepage_title(driver):
    homepage = HomePage(driver)
    homepage.open_home_page()
    time.sleep(10)



