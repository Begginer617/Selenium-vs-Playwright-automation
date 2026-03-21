from selenium import webdriver


class DriverFactory:
    @staticmethod
    def get_driver(browser_type="chrome"):
        # Skoro uruchamiasz z Windowsa, uderzasz w localhost:4444
        executor_url = "http://localhost:4444/wd/hub"

        if browser_type.lower() == "chrome":
            options = webdriver.ChromeOptions()
            # Opcjonalne: jeśli chcesz widzieć co się dzieje, nie dodawaj headless.
            # Grid w Dockerze i tak obsłuży to w swoim "wirtualnym" ekranie.

            driver = webdriver.Remote(
                command_executor=executor_url,
                options=options
            )
        else:
            raise Exception(f"Na ten moment wspieramy tylko Chrome w Dockerze!")

        driver.maximize_window()
        return driver