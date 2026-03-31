   ## Selenium-vs-Playwright-automation
   
   ## README — Docker Selenium vs. Playwright – Automation – A Final Project for a Postgraduate Studies in Test Automation

---

## 🧱 Project Architecture
The environment is orchestrated via **Docker Compose** and includes:
* **Selenium Grid 4** (Hub + Chrome Node) – for Selenium execution.
* **Playwright** (Python Container) – isolated environment for Playwright tests.
* **noVNC** (Port 7900) – real-time browser preview **(No password required)**.
* **Allure Docker Service** – automatic report generation + Web UI.

---

## 📁 Project Structure
* `/docker` – infrastructure configuration (`docker-compose.yml`).
* `/selenium_tests` – Selenium tests (integrated with `conftest.py`).
* `/playwright_tests` – Playwright tests.
* `/pages` – Page Object Model (POM) implementation.

---

## 🐳 Environment Management (Docker)

### How to Start the Environment:
From the project root directory, run:
powershell
cd docker
docker-compose up -d

Checking Status:
docker ps

Service URLs:
Service	         URL	                  Description
Selenium Grid UI	http://localhost:4444	Monitor Grid nodes and sessions
VNC Live Preview	http://localhost:7900	Watch tests in real-time (No password)
Allure Report UI	http://localhost:5252	View automated test reports

🧪 Running Tests
1. Selenium Tests (Hybrid Mode)
The conftest.py file allows you to toggle between local and remote execution using the custom --remote flag.


Run on Docker (Remote Mode):
# Execute from the project root directory
python -m pytest --remote true -v


# Execute from the project root directory (local)
python -m pytest --remote false -v


docker exec -it playwright bash
pytest .

📊 Allure Reporting
The system automatically watches the results directory and updates the report.

Live Report (UI): http://localhost:5252

Local Visualization (Optional):
allure serve reports/allure-results



🛑 Stopping the Environment
cd docker
docker-compose down


🔐 Test Credentials
Email: jaxons.danniels@company.com

Password: User1234


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
| Hub Port: 4444              |  | Pytest          |  | UI: 5252    |
+--------------+--------------+  +--------+--------+  +------+------+
   ```




