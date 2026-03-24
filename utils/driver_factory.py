from selenium import webdriver


class DriverFactory:
    @staticmethod
    def get_driver(browser_type="chrome"):
        # --- PRZEŁĄCZNIK ---
        # True = Docker (Prezentacja/VNC port 7900)
        # False = Lokalny Windows (Widzisz okno Chrome u siebie)
        run_remote = False

        if browser_type.lower() == "chrome":
            options = webdriver.ChromeOptions()

            if run_remote:
                # Opcja dla DOCKERA (Remote)
                executor_url = "http://localhost:4444/wd/hub"
                driver = webdriver.Remote(
                    command_executor=executor_url,
                    options=options
                )
            else:
                # Opcja LOKALNA (Windows)
                driver = webdriver.Chrome(options=options)
        else:
            raise Exception(f"Only chrome supported")

        driver.maximize_window()
        return driver