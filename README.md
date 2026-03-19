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
   
   
   
+--------------------------------------------------+
|                  Selenium Grid                   |
|                       HUB                        |
|              http://localhost:4444               |
+-----------------------------+--------------------+
                              |
                              |
+-----------------------------v--------------------+
|                   Chrome Node                    |
|             selenium/node-chrome                 |
|                    VNC: 5900                     |
+--------------------------------------------------+


+--------------------------------------------------+
|               Playwright Container               |
|   mcr.microsoft.com/playwright/python            |
|                                                  |
|   - uruchamianie testów                          |
|   - dostęp do Allure results                     |
+--------------------------------------------------+


+--------------------------------------------------+
|               Allure Docker Service              |
|                                                  |
|   +---------------------------+                  |
|   |     allure-generator      |                  |
|   |        port: 5050         |                  |
|   +-------------+-------------+                  |
|                 |                                |
|   +-------------v-------------+                  |
|   |          allure-ui        |                  |
|   |   http://localhost:5252   |                  |
|   +---------------------------+                  |
+--------------------------------------------------+


+--------------------------------------------------+
|                      Docker                      |
|               docker-compose.yml                 |
|          zarządza całym środowiskiem             |
+--------------------------------------------------+               
   
   
   
   
   
   
