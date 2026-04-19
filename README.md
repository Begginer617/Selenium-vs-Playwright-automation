## Selenium-vs-Playwright-automation

## README — Selenium vs Playwright Thesis Project
### Final project for postgraduate studies in Test Automation

---

# 🧱 Project Overview

This repository compares two UI automation frameworks on the same e-commerce flows:

- **Selenium** (POM + pytest)
- **Playwright** (POM + pytest-playwright)

The goal is a fair, repeatable, and measurable comparison of:

- stability,
- runtime,
- and implementation quality.

Current automated coverage:

- `7` Selenium test files (`8` total test cases, including parametrized scenario)
- `7` Playwright test files (`8` total test cases, including parametrized scenario)

---

# 📁 Project Structure

- `/docker` — infrastructure (`docker-compose.yml`)
- `/selenium_tests` — Selenium tests + fixtures
- `/playwright_tests` — Playwright tests + fixtures
- `/pages` — Page Object Model (POM) for both frameworks
- `/reports` — Allure raw results and generated reports

---

# 🐳 Docker Environment

The environment is orchestrated with Docker Compose and includes:

- **Selenium Grid 4** (Hub + Chrome Node)
- **Playwright runtime container**
- **noVNC** (`7900`) for live browser preview
- **Allure Docker Service** (`5050` API + `5252` UI)

## Start services

```bash
cd docker
docker-compose up -d
docker ps
```

## Service URLs

| Service | URL | Description |
| :--- | :--- | :--- |
| Selenium Grid UI | http://localhost:4444 | Grid status / active sessions |
| noVNC Preview | http://localhost:7900 | Live browser view |
| Allure UI | http://localhost:5252 | Report dashboard |

---

# 🧪 Running Tests

> Use `python` in local `.venv`.  
> In Linux/CI use `python3`.

## Selenium

Selenium execution is **always headed (non-headless)** in this project for consistent comparison with thesis assumptions.  
The `--headless` flag is kept only for CLI compatibility and is ignored for Selenium.

### Local execution

```bash
python3 -m pytest selenium_tests --remote false -v
```

### Docker Grid execution

```bash
python3 -m pytest selenium_tests --remote true -v
```

## Playwright

Install browser binaries once:

```bash
python3 -m playwright install chromium
```

Run suite:

```bash
python3 -m pytest playwright_tests -v
```

---

# ⏱️ Per-test Runtime Profiling (pytest --durations)

Runtime profiling is enabled globally in `pytest.ini`:

- `--durations=0` (display duration for all tests)
- `--durations-min=0.1` (mark tests slower than 0.1s)

### Example: show top 20 slowest Selenium tests

```bash
python3 -m pytest selenium_tests --durations=20 --durations-min=0.2 -v
```

### Example: compare total runtime framework vs framework

```bash
python3 -m pytest selenium_tests -q
python3 -m pytest playwright_tests -q
```

---

# 🧪 How to Reproduce Thesis Benchmark

Use this sequence to reproduce a fair Selenium vs Playwright benchmark on the same machine.

## 1) Prepare clean environment

- close unnecessary applications/processes,
- use the same Python virtual environment for both runs,
- do not run other browser-heavy workloads in parallel.

Optional (Docker mode):

```bash
cd docker
docker-compose up -d
cd ..
```

## 2) Clear previous artifacts

```bash
rm -rf reports/allure-results
mkdir -p reports/allure-results
```

On Windows PowerShell:

```powershell
Remove-Item -Recurse -Force reports/allure-results -ErrorAction SilentlyContinue
New-Item -ItemType Directory -Path reports/allure-results | Out-Null
```

## 3) Run Selenium benchmark

Selenium runs in non-headless mode.

```bash
python3 -m pytest selenium_tests -v -p allure_pytest --alluredir=reports/allure-results --durations=0 --durations-min=0.1
```

Record:

- total runtime from pytest summary,
- pass/fail counts,
- top slow tests from durations table.

## 4) Run Playwright benchmark

Playwright also runs in non-headless mode (configured with `headless: false` in `playwright_tests/conftest.py`).

```bash
python3 -m pytest playwright_tests -v -p allure_pytest --alluredir=reports/allure-results --durations=0 --durations-min=0.1
```

Record the same metrics:

- total runtime,
- pass/fail,
- slowest tests.

## 5) Compare results in thesis table

Recommended columns:

- Framework
- Total tests
- Passed
- Failed
- Total runtime (s)
- Slowest test name
- Slowest test runtime (s)
- Notes (timeouts/flaky behavior)

## 6) Repeatability recommendation

For stronger methodology, run each framework at least 3 times and report:

- mean runtime,
- min/max runtime,
- standard deviation (optional).

---

# 📊 Allure Reporting

## Generate raw results

```bash
python3 -m pytest selenium_tests --remote false -v -p allure_pytest --alluredir=reports/allure-results
python3 -m pytest playwright_tests -v -p allure_pytest --alluredir=reports/allure-results
```

## Serve report locally

```bash
allure serve reports/allure-results
```

## Docker Allure UI

With Docker services running, open:

```bash
http://localhost:5252
```

Volume mapping:

- Local: `./reports/allure-results`
- Container: `/app/allure-results`

---

# ✅ Current Status (refactor-final)

- Selenium suite: `8 passed` (latest verified baseline before additional optimizations)
- Playwright suite: `8 passed`

---

# 🔐 Test Credentials

```text
Email: jaxons.danniels@company.com
Password: User1234
```

---

# 🛠️ Troubleshooting

## 1) `allure: command not found`

```bash
allure --version
```

If missing, install Allure CLI and reopen terminal.

## 2) `JAVA_HOME is not set`

Allure requires Java:

- install JDK (Temurin 17/21 recommended),
- set `JAVA_HOME`,
- add `%JAVA_HOME%/bin` to PATH.

## 3) Playwright browser launch issues

```bash
python -m playwright install chromium
```

## 4) Selenium Grid startup issues

```bash
cd docker
docker-compose down
docker-compose up -d
```

## 5) Allure UI shows no results

- run tests with `--alluredir=reports/allure-results`, and
- ensure Docker can access `./reports/allure-results`.

## 6) Port conflict (4444 / 5252 / 7900)

Stop conflicting process/container and restart services.

---

# 🛑 Stopping Docker Environment

```bash
cd docker
docker-compose down
cd ..
```

Alternative:

```bash
docker-compose -f docker/docker-compose.yml down
```






















