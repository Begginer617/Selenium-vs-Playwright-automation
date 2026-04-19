## Selenium-vs-Playwright-automation

## README — Docker Selenium vs. Playwright Automation  
### Final project for postgraduate studies in Test Automation

---

# 🧱 Project Architecture

The environment is orchestrated via **Docker Compose** and includes:

- **Selenium Grid 4** (Hub + Chrome Node) — Selenium execution
- **Playwright container** — isolated Playwright runtime
- **noVNC** (`7900`) — live browser preview (**no password**)
- **Allure Docker Service** (`5050` API + `5252` UI) — report generation and UI

---

# 📁 Project Structure

- `/docker` — infrastructure (`docker-compose.yml`)
- `/selenium_tests` — Selenium tests + fixtures
- `/playwright_tests` — Playwright tests + fixtures
- `/pages` — Page Object Model (POM)
- `/reports` — Allure raw results and generated reports

---

# 🐳 Environment Management (Docker)

## Start environment

Run from project root:

```bash
cd docker
docker-compose up -d
docker ps
```

## Service URLs

| Service | URL | Description |
| :--- | :--- | :--- |
| Selenium Grid UI | http://localhost:4444 | Grid status / node sessions |
| VNC Live Preview | http://localhost:7900 | Live browser preview |
| Allure Report UI | http://localhost:5252 | Test report dashboard |

---

# 🧪 Running Tests

> Use `python` in your local `.venv`.  
> In Linux/CI environments (like this cloud run), use `python3`.

## Selenium test modes (`selenium_tests/conftest.py`)

- `--remote true` → run on Selenium Grid (Docker)
- `--remote false` → run locally
- Selenium is forced to run in headed mode (non-headless) for consistent thesis comparison

### Selenium — local (headed)

```bash
python3 -m pytest selenium_tests --remote false -v
```

### Selenium — Docker Grid (remote)

```bash
python3 -m pytest selenium_tests --remote true -v
```

## Per-test runtime profiling

`pytest.ini` now enables duration profiling by default:

- `--durations=0` (show runtime for all tests)
- `--durations-min=0.1` (highlight tests slower than 0.1s)

You can still override thresholds from CLI, e.g.:

```bash
python3 -m pytest selenium_tests --durations=20 --durations-min=0.2 -v
```

## Playwright tests

Install browsers once (local execution):

```bash
python3 -m playwright install chromium
```

Run suite:

```bash
python3 -m pytest playwright_tests -v
```

---

# ✅ Current verified status

Latest full verification on `refactor-final`:

- Selenium suite: `8 passed`
- Playwright suite: `8 passed`

Commands used:

```bash
python3 -m pytest selenium_tests -q
python3 -m pytest playwright_tests -q
```

---

# 📊 Allure Reporting

## Local Allure CLI (optional)

Generate raw results:

```bash
python3 -m pytest selenium_tests --remote false -v -p allure_pytest --alluredir=reports/allure-results
python3 -m pytest playwright_tests -v -p allure_pytest --alluredir=reports/allure-results
```

Serve report locally:

```bash
allure serve reports/allure-results
```

## Docker Allure Service

When Docker services are running, open:

```bash
http://localhost:5252
```

### Mapping used by docker-compose

- Local: `./reports/allure-results`
- Container: `/app/allure-results`

---

# 🛑 Stopping the Environment

From project root:

```bash
cd docker
docker-compose down
cd ..
```

Alternative (without changing directory):

```bash
docker-compose -f docker/docker-compose.yml down
```

---

# 🔐 Test Credentials

```text
Email: jaxons.danniels@company.com
Password: User1234
```

---

# 🛠️ Troubleshooting

## 1) `allure: command not found`

- Reopen terminal after installing Allure CLI
- Verify:

```bash
allure --version
```

## 2) `JAVA_HOME is not set`

Allure requires Java.

- Install JDK (Temurin 17/21 recommended)
- Set `JAVA_HOME`
- Add `%JAVA_HOME%/bin` to PATH

## 3) Playwright cannot launch browser

Install browser binaries:

```bash
python -m playwright install chromium
```

## 4) Selenium Grid/node startup issues

```bash
cd docker
docker-compose down
docker-compose up -d
```

## 5) Allure UI opens but no results

- Ensure tests were run with `--alluredir=reports/allure-results` (local CLI mode), or
- Ensure Docker has access to `./reports/allure-results` (Docker mode)

## 6) Port already allocated

Check what process/container uses the port and free it (e.g., 4444 / 5252 / 7900).






















