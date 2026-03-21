   # Selenium-vs-Playwright-automation
   
   # README — Docker Selenium vs. Playwright – Automation – A Final Project for a Postgraduate Studies in Test Automation
   
   🚀 Overview
   This project provides a complete automated testing environment using:
   - Selenium Grid 4 (Hub + Chrome Node)
   - Playwright (Python)
   - Allure Docker Service (report generator + UI)
   - Docker Compose for orchestration
   The environment allows running Selenium tests on a distributed Grid and Playwright tests inside a dedicated container, with reporting handled by Allure.
   
   🧱 Project Structure
   /docker
      docker-compose.yml
   /playwright_tests
   /selenium_tests

   FOR 💻 Local Development (Windows / PyCharm)
   1. Installatiion
   pip install -r requirements.txt

   2.Running test with Selenium (z Windowsem conetting with Gride in Docker)
   python -m pytest selenium_tests/ --alluredir=reports/allure-results

   3. Allure report visuallisation
   allure serve reports/allure-results

   4. Downloading Allure report 
   allure generate reports/allure-results -o reports/allure-report --clean

   Important info:
   This will create an `allure-report` folder containing a ready-to-use `index.html` file. 
   Note: Due to browser security restrictions, you cannot simply double-click to open it (it will be empty). 
   It must be served by a server (such as your Docker Allure UI running on localhost:5252).

   
   FOR DOCKER
   
   🐳 How to Start the Environment
   From the docker directory run:
   docker compose up -d
   
   This will:
   - pull all required images (first run only),
   - start all containers in the background.
   
   🔍 How to Check if Everything Is Running
   docker ps
   
   You should see containers:
   - selenium-hub
   - chrome
   - playwright
   - allure-generator
   - allure-ui
   All with status Up.
   
   🌐 Service URLs
   ✔ Selenium Grid UI
   http://localhost:4444
   
   ✔ Allure Report UI
   http://localhost:5252
   
   🧪 Running Tests
   ▶ Playwright tests (inside container)
   docker exec -it playwright bash
   pytest .
   
   
   ▶ Selenium tests (local or container)
   Use the remote WebDriver URL:
   http://selenium-hub:4444/wd/hub
   
   Example:
   webdriver.Remote(
       command_executor="http://selenium-hub:4444/wd/hub",
       options=ChromeOptions()
   )
   
   
   📊 Generating Allure Reports
   Allure Docker Service automatically watches the results directory.
   To trigger report generation manually:
   curl -X POST http://localhost:5252/generate-report
   
   🛑 Stopping the Environment
   docker compose down
   
   To remove volumes as well:
   docker compose down -v
   
   🔄 Restarting
   docker compose restart
   
   🧹 Cleaning Up Docker (optional)
   docker system prune -a

   ENV
   CREDENTIALS:
   Email: jaxons.danniels@company.com
   Password: User1234
   
   
## Architecture

```text
[+--------------------------------------------------------------+
|                        Selenium Grid                         |
|                              HUB                             |
|                    http://localhost:4444                     |
+-------------------------------+------------------------------+
                                |
                                |
+-------------------------------v------------------------------+
|                          Chrome Node                         |
|                   selenium/node-chrome                       |
|                          VNC: 5900                           |
+--------------------------------------------------------------+


+--------------------------------------------------------------+
|                     Playwright Container                     |
|            mcr.microsoft.com/playwright/python               |
|                                                              |
|                - uruchamianie testów                         |
|                - dostęp do Allure results                    |
+--------------------------------------------------------------+


+--------------------------------------------------------------+
|                     Allure Docker Service                    |
|                                                              |
|   +-------------------------------+                          |
|   |        allure-generator       |                          |
|   |            port: 5050         |                          |
|   +---------------+---------------+                          |
|                   |                                          |
|   +---------------v---------------+                          |
|   |             allure-ui         |                          |
|   |      http://localhost:5252    |                          |
|   +-------------------------------+                          |
+--------------------------------------------------------------+


+--------------------------------------------------------------+
|                            Docker                            |
|                     docker-compose.yml                       |
|                zarządza całym środowiskiem                   |
+--------------------------------------------------------------+]
