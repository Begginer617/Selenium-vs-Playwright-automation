   ## Selenium-vs-Playwright-automation
   
   ## README — Docker Selenium vs. Playwright – Automation – A Final Project for a Postgraduate Studies in Test Automation

---

# 🧱 Project Architecture

The environment is orchestrated via **Docker Compose** and includes:
* **Selenium Grid 4** (Hub + Chrome Node) – for Selenium execution.
* **Playwright** (Python Container) – isolated environment for Playwright tests.
* **noVNC** (Port 7900) – real-time browser preview **(No password required)**.
* **Allure Docker Service** – automatic report generation + Web UI.

---

# 📁 Project Structure

* `/docker` – infrastructure configuration (`docker-compose.yml`).
* `/selenium_tests` – Selenium tests (integrated with `conftest.py`).
* `/playwright_tests` – Playwright tests.
* `/pages` – Page Object Model (POM) implementation.
---

# 🐳 Environment Management (Docker)

## How to Start the Environment:
From the project root directory, run:
Checking Status:
docker ps

->powershell
->cd docker
->docker-compose up -d 


## Service URLs:
```bash
Service	            URL	                    Description
Selenium Grid UI	http://localhost:4444	Monitor Grid nodes and sessions
VNC Live Preview	http://localhost:7900	Watch tests in real-time (No password)
Allure Report UI	http://localhost:5252	View automated test reports
```


## 🧪 Running Tests
1. Selenium Tests (Hybrid Mode)
The conftest.py file allows you to toggle between local and remote execution using the custom --remote flag.

--remote true   → run tests inside Docker (Selenium Grid)

--remote false  → run tests locally on your machine


## 🐳 Run Selenium tests in Docker (REMOTE mode)
(recommended for CI / reproducible environment). Execute from the project root directory:

### python -m pytest selenium_tests --remote true -v


➡️ Tests run inside Docker

➡️ Results are automatically collected by Allure Docker Service

➡️ Report available at:
```bash
http://localhost:5252
```


💻 Run Selenium tests locally (LOCAL mode)
(useful for debugging without Docker)

# Execute from the project root directory (local)

### 
```bash
python -m pytest selenium_tests -v -p allure_pytest --alluredir=reports/allure-results
```

## 🏎️ Execution Modes

| Mode | Command | Description |
| :--- | :--- | :--- |
| **Standard** | `python -m pytest selenium_tests --remote false` | Runs tests locally with visible browser. |
| **Headless** | `python -m pytest selenium_tests --remote false --headless true` | Runs tests locally in the background (faster). |
| **Docker** | `python -m pytest selenium_tests --remote true` | Runs tests on Selenium Grid inside Docker. |


# Then generate a local report (optional):
```bash
allure serve reports/allure-results
```


⚠️ Important:
Local Allure CLI works only with results generated locally.
Remote (Docker) results are handled by Allure Docker Service.

To ensure Allure collects your data correctly, notice the difference in directory mapping:

Local Execution (--remote false):
Tests write to

### ./reports/allure-results. 

The Allure CLI on your machine reads from this local folder.

Docker Execution (--remote true):
Tests run inside the container where the project root is /app. Results are written to 

### /app/reports/allure-results.


The docker-compose.yml maps local ./reports folder to the container's /app/reports. This allows the Allure Docker Service to see the results instantly.


FOR Playwright ( in progress, not finished)
docker exec -it playwright bash
pytest .

## 📊 Allure Reporting
Automatic reporting (Docker mode)
When running tests with --remote true, results are sent to:
allure-docker-service

## Live report UI:
👉 
```bash
http://localhost:5252
```
No manual steps required.


Local reporting (optional)
Only for tests run with --remote false:
```bash
allure serve reports/allure-results
```



🛑 Stopping the Environment
cd docker
```bashdocker-compose down
```


🔐 Test Credentials
```bash
Email: jaxons.danniels@company.com
```

```bash
Password: User1234
```bash


## Architecture

 ```bash
      +-------------------------------------------------------+
      |                  DOCKER NETWORK                       |
      |          (Managed by docker-compose.yml)              |
      +-------+--------------------------+-------------+------+
              |                          |             |
+--------------v--------------+  +--------v--------+  +-v-----------+
|    SELENIUM GRID            |  |   PLAYWRIGHT    |  |   ALLURE    |
| (Hub:4444 + Chrome Node)    |  |   CONTAINER     |  |   SERVICE   |
+-----------------------------+  +-----------------+  +-------------+
| VNC Port: 7900 (No Login)   |  | Python 3.14     |  | API: 5050   |
| Hub Port: 4444              |  | Pytest          |  | UI:  5252   |
+--------------+--------------+  +--------+--------+  +------+------+
   ```

🛠️ Troubleshooting Guide
This section covers the most common issues you may encounter when running the environment, executing tests, or generating reports.

❌ 1. allure: command not found
Cause
Allure CLI is not available in your system PATH, or the terminal was opened before installation.
Fix
- Close all terminals.
- Open a new PowerShell window.
- Verify installation:
allure --version

If it still fails:
- Check if Scoop installed Allure:
scoop list
- Add Allure manually to PATH:
C:\Users\<USER>\scoop\apps\allure\current\bin


❌ 1. allure: command not found
Cause
Allure CLI is not available in your system PATH, or the terminal was opened before installation.
Fix
1. Close all terminals.
2. Open a new PowerShell window.
3. Verify installation:
allure --version

If it still fails:
1. Check if Scoop installed Allure:
scoop list
2. Add Allure manually to PATH:
C:\Users\<USER>\scoop\apps\allure\current\bin

❌ 2. JAVA_HOME is not set
Cause
Allure CLI requires Java, but your system cannot locate a JDK installation.
Fix
1. Install Temurin JDK (17 or 21 recommended):
https://adoptium.net
- Set the environment variable:
2. 	Set the environment variable:
JAVA_HOME = C:\Program Files\Eclipse Adoptium\jdk-XX
3. Add to PATH:
%JAVA_HOME%\bin
4. Verify:
->powershell
java -version
echo $env:JAVA_HOME

❌ 3. Allure report is empty
Cause
You ran tests in remote mode, so results were generated inside Docker, not locally.
Fix
For local Allure CLI:
1. Run tests locally:
pytest selenium_tests --remote false -v --alluredir=reports/allure-results
2. Then:
allure serve reports/allure-results

For Docker Allure Service:
Open:
👉 http://localhost:5252

❌ 4. Allure Docker Service shows no results

Cause
The container cannot access the results directory, or tests are writing to the wrong path.
Fix
1. Ensure your docker-compose.yml includes:
- ./reports:/app/reports
2. And tests in remote mode write to:
/app/reports/allure-results


❌ 5. Selenium Grid does not start / Chrome Node cannot connect
Cause
Port conflicts, stale containers, or network issues.
Fix
1. Stop the environment:
docker-compose down
2. Clean unused containers:
docker system prune -f
3. Restart:
docker-compose up -d


❌ 6. VNC (port 7900) not accessible
Cause
Port 7900 is already in use or the Selenium container failed to start.
Fix
1. Check running containers:
docker ps
2. Check port usage:
netstat -ano | findstr 7900
3. If needed, change the port in docker-compose.yml:
- "7901:7900"

❌ 7. Playwright error: Failed to launch browser
Cause
Playwright browsers are not installed inside the container.
Fix
1. Inside the Playwright container:
playwright install


❌ 8. Selenium tests fail locally
Cause
The --remote true flag forces Docker execution.
Fix
1. Run tests locally:
pytest selenium_tests --remote false -v

❌ 9. Docker error: port is already allocated
Cause
Another process is using the same port (e.g., 4444 or 5252).
Fix
1. Find the process:
netstat -ano | findstr 4444
2. Terminate it:
taskkill /PID <PID> /F

❌ 10. Allure Docker Service UI loads, but report is empty
Cause
The results directory is empty.
Fix
1. Check:
ls reports/allure-results


If empty → tests did not generate results.
1. Verify your pytest command includes:
--alluredir=/app/reports/allure-results






















