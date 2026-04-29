# Selenium vs Playwright — UI Test Automation

Postgraduate / portfolio project comparing **Selenium 4** and **Playwright** on the same **Telerik Kendo UI eShop** demo (`demos.telerik.com`). Both stacks use **pytest**, **Page Object Model (POM)**, and optional **Allure** reporting.

---

## 1. Project description

### What it does

- Automates the same high-level user flows twice: once with **Selenium + Chrome**, once with **Playwright**.
- Targets a public demo e-commerce app so results are reproducible without a private backend.

### Problem it addresses

- Provides a **fair, side-by-side** comparison of frameworks for the same scenarios (login, registration validation, header navigation, product listing/sort/filters, basket, multi-item totals).
- Collects evidence for **stability**, **runtime**, and **maintainability** (structure, waits, flakiness).

### Technologies (from `requirements.txt` and code)

| Area | Stack |
|------|--------|
| Language | Python 3 |
| Test runner | **pytest** 9.x |
| Selenium | **selenium** 4.x, **WebDriverWait**, Chrome (local or Grid) |
| Playwright | **playwright**, **pytest-playwright** |
| Parallel runs | **pytest-xdist** |
| Reporting | **allure-pytest** |
| Other | **requests**, **mysql-connector-python** (deps in file; DB not required for UI tests) |

---

## 2. Project structure

```
.
├── conftest.py                 # Root: registers --remote and --headless for Selenium (early pytest hook)
├── pytest.ini                  # Global pytest defaults, testpaths, markers
├── requirements.txt            # Python dependencies (pin versions)
├── README.md                   # This file
│
├── docker/
│   └── docker-compose.yml      # Selenium Grid hub + Chrome node, Playwright image, Allure services
│
├── selenium_tests/             # Selenium test package
│   ├── conftest.py             # Session driver, reset_browser_state, page fixtures, Allure screenshot hook
│   ├── test_*.py               # Test modules (login, home, header, basket, registration, search/sort, multi-item)
│   └── ...
│
├── playwright_tests/           # Playwright test package
│   ├── conftest.py             # Page fixtures, browser_context_args, launch args, Allure on failure
│   ├── pytest.ini              # pythonpath for this subtree (used when running from this folder)
│   └── test_*.py               # Mirror flows to Selenium (naming includes minor typos in filenames)
│
├── pages/
│   ├── selenium/               # Selenium Page Objects (inherit BasePage)
│   │   ├── base_page_selenium.py
│   │   ├── home_page_selenium.py
│   │   ├── login_page_selenium.py
│   │   ├── header_page_selenium.py
│   │   ├── products_page_selenium.py
│   │   └── registration_page_selenium.py
│   └── playwright/             # Playwright Page Objects
│       ├── base_page_playwright.py
│       ├── home_page_playwright.py
│       ├── login_page_playwright.py
│       ├── header_page_playwright.py
│       ├── products_page_playwright.py
│       └── registration_page_playwright.py
│
├── utils/
│   └── config.py               # Shared constants (BASE_URL, demo credentials, default timeout)
│
└── reports/                    # Optional: Allure raw results / generated HTML (create locally; see Docker volume)
```

| Path | Role |
|------|------|
| **`conftest.py` (root)** | Registers **`--remote`** and **`--headless`** so `pytest selenium_tests/ ...` parses them reliably. |
| **`pytest.ini`** | `pythonpath = .`, discovers `selenium_tests` and `playwright_tests`, `--durations`, marker `flaky`. |
| **`selenium_tests/conftest.py`** | Chrome `Options`, session-scoped `driver`, light vs heavy browser reset, `DriverFactory` (local vs `localhost:4444`). |
| **`playwright_tests/conftest.py`** | `page`-based fixtures, `base_url`, headed launch defaults, Allure screenshot on failure. |
| **`pages/selenium/`** | Encapsulates locators + waits + actions for Selenium. |
| **`pages/playwright/`** | Same idea for Playwright (`page` API). |
| **`utils/config.py`** | Central URL and test user constants (credentials also documented below). |

---

## 3. How to run tests

Use a virtual environment (recommended).

### Install dependencies

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate

pip install -r requirements.txt
```

### Playwright browsers (required for Playwright tests)

```bash
python -m playwright install chromium
```

### Selenium — local Chrome

```bash
python -m pytest selenium_tests/ --remote false -v
```

### Selenium — headless Chrome

Uses Chrome flag `--headless=new` (requires root `conftest.py` so the option is registered).

```bash
python -m pytest selenium_tests/ --remote false --headless true -v
```

### Selenium — Docker Grid (`localhost:4444`)

Start Grid first (see [Docker](#docker-optional)).

```bash
python -m pytest selenium_tests/ --remote true -v
```

### Selenium — parallel (`pytest-xdist`)

Each worker gets its own browser session. Ensure enough machine resources and, for `--remote true`, enough Grid sessions.

```bash
python -m pytest selenium_tests/ -n auto -q
```

Combine with headless:

```bash
python -m pytest selenium_tests/ --headless true -n auto -q
```

### Playwright

From repo root (uses root `pytest.ini`):

```bash
python -m pytest playwright_tests/ -v
```

Or from `playwright_tests/` (uses local `pytest.ini` + `pythonpath`):

```bash
cd playwright_tests
python -m pytest -v
cd ..
```

### Run both suites (default discovery)

```bash
python -m pytest -v
```

### Slowest tests (built into `pytest.ini`)

```bash
python -m pytest selenium_tests/ --durations=15
```

### Allure results

```bash
python -m pytest selenium_tests/ -v --alluredir=reports/allure-results
python -m pytest playwright_tests/ -v --alluredir=reports/allure-results
allure serve reports/allure-results
```

Install [Allure Commandline](https://github.com/allure-framework/allure2) and Java if `allure` is not on PATH.

---

## 4. System requirements

| Requirement | Notes |
|-------------|--------|
| **Python** | 3.10+ recommended (project tested with 3.12/3.13 in CI-like environments). |
| **pip** | For `requirements.txt`. |
| **Chrome** | Selenium local runs use **Google Chrome**; match **ChromeDriver** (Selenium Manager in 4.x usually resolves this). |
| **Playwright** | `playwright install chromium` after `pip install`. |
| **Docker** (optional) | For Grid + Allure stack (`docker/docker-compose.yml`). |
| **Network** | Tests hit **https://demos.telerik.com** — stable internet required. |
| **Java** | Only if you generate/serve Allure reports via CLI. |

---

## 5. How the framework works

### Page Object Model (POM)

- Tests stay thin; **locators and waits** live under `pages/selenium/` and `pages/playwright/`.
- **Selenium**: classes inherit `BasePage` (`wait_for_visible`, `safe_click`, `open`, etc.).
- **Playwright**: page classes wrap `page` (`goto`, `locator`, `expect` patterns in each file).

### Fixtures

| Framework | Key fixtures |
|-----------|----------------|
| **Selenium** | `driver` (session), `reset_browser_state` (autouse, per test), `*_page_selenium` factories. |
| **Playwright** | `page` (from pytest-playwright), `browser_context_args`, `browser_type_launch_args`, `*_pw` fixtures. |

### Setup / teardown (Selenium)

- **Session-scoped `driver`**: one browser per pytest worker.
- **Heavy reset once** after driver start: navigate to eShop origin + CDP `Storage.clearDataForOrigin` + `Network.clearBrowserCache` (IndexedDB / cache).
- **Light reset before each test**: `get` eShop entry URL + delete cookies + clear `localStorage` / `sessionStorage` (faster than repeating full CDP every test).

### Base pages

- `pages/selenium/base_page_selenium.py` — shared waits, clicks, navigation helpers.
- `pages/playwright/base_page_playwright.py` — shared Playwright helpers.

### Utils

- `utils/config.py` — `BASE_URL`, demo `USER_EMAIL` / `USER_PASSWORD`, `DEFAULT_TIMEOUT`, optional `SELENIUM_HUB` string.

### Demo credentials (public demo user)

```text
Email:    jaxons.danniels@company.com
Password: User1234
```

---

## 6. Adding a new test

1. **Choose stack**: `selenium_tests/test_<feature>_selenium.py` or `playwright_tests/test_<feature>_playwright.py`.
2. **Import** Allure markers if needed (`@allure.suite`, etc., match existing style).
3. **Request fixtures**: e.g. `home_page_selenium`, `login_page_selenium`, `product_page_selenium` or `page`, `login_page_pw`, …
4. **Call page methods** in the same order as the user story; keep assertions readable (`assert` + message).
5. **Run**: `python -m pytest path/to/test_file.py -v`.
6. **Optional**: add `-p allure_pytest --alluredir=reports/allure-results` for reporting.

Do not rely on another test having run first; use fixtures and POM methods to reach a known state.

---

## 7. Adding a new Page Object

### Selenium

1. Create `pages/selenium/<name>_page_selenium.py`.
2. Subclass `BasePage`; store **locators** as class attributes `(By.…, "…")`.
3. Implement methods using `self.wait_for_*`, `self.click`, `self.open`, etc.
4. Register a **pytest fixture** in `selenium_tests/conftest.py` that returns `YourPage(self.driver)`.

### Playwright

1. Create `pages/playwright/<name>_page_playwright.py`.
2. Accept `page` in `__init__` (see existing pages).
3. Use `self.page.goto`, locators, and `expect` where appropriate.
4. Add a **fixture** in `playwright_tests/conftest.py`.

Keep framework-specific code in the correct `pages/` subtree so imports stay clear.

---

## 8. CI/CD

There is **no** `.github/workflows/` (or similar) in this repository at the time of writing. For CI, a typical job would:

1. `pip install -r requirements.txt`
2. `playwright install chromium --with-deps` (Linux agents)
3. Install Chrome + run Selenium with `--headless true` or use a Selenium service container
4. `pytest` with optional `-n auto` and `--alluredir`, then upload Allure artifacts

---

## 9. Known issues & troubleshooting

| Symptom | What to check |
|---------|----------------|
| **`unrecognized arguments: --headless`** | Ensure **`conftest.py` exists at repository root** (registers CLI options before nested conftests). Pull latest `main` / branch. |
| **Selenium Grid connection errors** | `docker compose up` in `docker/`, then `--remote true`. Hub: `http://localhost:4444`. |
| **`pytest.mark.flaky` warning** | Register the marker in `pytest.ini` or install `pytest-rerunfailures` if you use `@pytest.mark.flaky`. |
| **Playwright `headless: False`** | Browsers open visibly by design in `playwright_tests/conftest.py`; change launch args for CI headless. |
| **Duplicate `browser_context_args` in Playwright conftest** | File currently defines the name twice — align with a single definition if you refactor (behaviour depends on which hook pytest keeps last). |
| **Flaky demo** | `demos.telerik.com` is shared and rate-limited; retries or longer waits may be needed on slow networks. |
| **Allure `command not found`** | Install Allure CLI + **JAVA_HOME**. |

---

## 10. Performance & stability tips (implemented or recommended)

- **Parallel Selenium**: `pytest -n auto` — each worker has its own session `driver` (`selenium_tests/conftest.py`).
- **Avoid implicit waits** with explicit `WebDriverWait` — Selenium uses `implicitly_wait(0)`.
- **Prefer explicit conditions** (`element_to_be_clickable`, `visibility_of_element_located`) over fixed sleeps (Selenium POM avoids `time.sleep` for sync).
- **Session vs per-test work**: heavy CDP storage/cache clear runs **once per session**; lighter cookie/storage reset runs **per test** for isolation.
- **Headless for throughput**: `--headless true` for local/CI when you do not need a visible window.
- **Stable selectors**: favour `ID`, `data-*`, or scoped CSS; XPath is used where the demo DOM requires it.
- **Direct URLs** where possible inside POM (`open`, `_get_url_fast`) to skip redundant clicks when the scenario allows.

---

## Docker (optional)

From repository root:

```bash
cd docker
docker compose up -d
```

Typical ports (see `docker/docker-compose.yml`):

| Service | Port | Purpose |
|---------|------|---------|
| Selenium Hub | 4444 | Grid / WebDriver endpoint |
| Chrome node | 7900 | noVNC preview |
| Allure API / UI | 5050 / 5252 | Report generation & dashboard |

Stop:

```bash
cd docker
docker compose down
```

---

## Changelog vs previous README (summary)

| Topic | Old README | Current state |
|--------|------------|----------------|
| **Headless Selenium** | Stated headless was ignored | **`--headless true`** is supported (Chrome `--headless=new`). |
| **Root `conftest.py`** | Not documented | Documented; required for `--headless` / `--remote` parsing. |
| **pytest-xdist** | Not mentioned | In `requirements.txt`; documented `-n auto`. |
| **Selenium reset** | Implied per-test heavy work | **Heavy CDP once per session**, light reset per test. |
| **Structure** | High-level only | Full tree + table for `pages/`, `utils/`, `docker/`. |
| **Playwright** | Basic run | Root vs `playwright_tests/` run, `install chromium`. |
| **CI/CD** | Not clearly stated | **No workflows in repo**; generic CI guidance added. |
| **Troubleshooting** | Partial | Expanded (headless, Grid, flaky marker, Playwright conftest note). |

---

## Future improvements (ideas)

- Add **GitHub Actions** workflow matrix (Selenium headed/headless + Playwright) with cached browsers.
- Resolve **duplicate `browser_context_args`** fixtures in `playwright_tests/conftest.py`.
- Optional **`Makefile`** or **`nox`** tasks for `lint`, `test-selenium`, `test-pw`, `allure`.
- **Pre-commit** (e.g. `ruff`) for consistent Python style.
- **Environment file** (`.env.example`) if secrets or base URLs move out of code.

---

## License / thesis

Use and cite this repository according to your institution’s rules for academic work. The automated target is a **public demo**; do not use production secrets in tests.
