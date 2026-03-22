   ## Selenium-vs-Playwright-automation
   
   ## README — Docker Selenium vs. Playwright – Automation – A Final Project for a Postgraduate Studies in Test Automation
   
   🚀 Overview
   Project Architecture
   The environment is orchestrated via Docker Compose and includes:
   Selenium Grid 4 (Hub + Chrome Node)
   Playwright (Python environment)
   Allure Docker Service (Report generation + Web UI)
   NoVNC (Real-time browser preview)
   
   🧱 Project Structure
   /docker
      docker-compose.yml
   /playwright_tests
   /selenium_tests

   FOR 💻 Local Development (Windows / PyCharm)
   1. Installatiion

   ```bash
   pip install -r requirements.txt
   ```

   2. To run tests from your local machine against the Docker Selenium Grid:
  
   ```bash
   python -m pytest selenium_tests/ --alluredir=reports/allure-results
   ```

   3. Allure report visuallisation

   Live Server:
   ```bash
   allure serve reports/allure-results
   ```

   Static Report Generation:

   ```bash
   allure generate reports/allure-results -o reports/allure-report --clean
   ```

   5. Downloading Allure report 

   ```bash
   allure generate reports/allure-results -o reports/allure-report --clean
   ```

   Important info:
   This will create an `allure-report` folder containing a ready-to-use `index.html` file. 
   Note: Due to browser security restrictions, you cannot simply double-click to open it (it will be empty). 
   It must be served by a server (such as your Docker Allure UI running on localhost:5252).

   
   ## FOR DOCKER

   Checking status of docker:

   ```bash
   docker ps
   ```

   IF not running DO steps below:
   
   🐳 How to Start the Environment
   From the project root directory, run:
   ```bash
   docker compose up -d
   ```
   
   This will:
   - pull all required images (first run only),
   - start all containers in the background.

   ```bash
   Service	         URL	                  Description
   Selenium Grid UI	http://localhost:4444	Manage and monitor Grid nodes
   VNC Live Preview	http://localhost:7900	Watch tests running in real-time (No password)
   Allure Report UI	http://localhost:5252	View automated test reports   
   ```
   ## 🔍 How to Check if Everything Is Running
   
  ```bash
   docker ps
   ```
   
   You should see containers:
   - selenium-hub
   - chrome
   - playwright
   - allure-generator
   - allure-ui
   All with status Up.
   
   🌐 Service URLs
   
   ✔ Selenium Grid UI
   
   ```bash
   http://localhost:4444
   ```

   ✔ Allure Report UI

   ```bash
   http://localhost:5252
   ```
   
   🧪 Running Tests
   ▶ Playwright tests (inside container)
   
   ```bash
   docker exec -it playwright bash
   pytest .
   ```
   
   
   ▶ Selenium tests (local or container)
   Use the remote WebDriver URL:

   ```bash
   http://selenium-hub:4444/wd/hub
   ```
   
   
   Example:
   ```bash
   webdriver.Remote(
       command_executor="http://selenium-hub:4444/wd/hub",
       options=ChromeOptions()
   )
   ```
   
   
   📊 Generating Allure Reports
   Allure Docker Service automatically watches the results directory.
   To trigger report generation manually:
   
   ```bash
   curl -X POST http://localhost:5252/generate-report
   ```
   
   🛑 Stopping the Environment
   
   ```bash
   docker compose down
   ```
   
   To remove volumes as well:
   
   ```bash
   docker compose down -v
   ```
   
   🔄 Restarting
   
   ```bash
   docker compose restart
   ```
   
   🧹 Cleaning Up Docker (optional)

   ```bash
   docker system prune -a
   ```
  
   ENV
   CREDENTIALS:
   
   Email:
   ```bash
   jaxons.danniels@company.com
   ```
   Password: 
   ```bash
   User1234
   ```
   
   
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
