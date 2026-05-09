# UI & API Test Suite

A comprehensive test framework combining UI tests (using Playwright) and API tests for automated testing with parallel execution, reporting, and CI/CD integration.

## Prerequisites

- **Python** 3.11 or higher
- **pip** (Python package manager)
- **Git** (for cloning and CI/CD)

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd qa-assignment-jonathan-chen
```

2. Install Python dependencies:
```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

3. Install Playwright browser binaries (required for UI tests):
```bash
python -m playwright install --with-deps
```

4. Configure test settings in `config.json`:
   - `base_url`: Website URL for UI tests
   - `api.base_url`: API endpoint for API tests
   - `credentials`: Username/password for login
   - `timeouts`: Wait times for elements and network requests

## How to Run Locally

### Run all tests
```bash
pytest
```

### Run only UI tests
```bash
pytest ui
```

### Run only API tests
```bash
pytest api
```

### Run a specific test
```bash
pytest ui/test_client_ui.py::test_login
```

## How to Run in Parallel

Run tests with 4 workers (execute multiple tests simultaneously):
```bash
pytest -n 4
```

Or use the default configuration (2 workers):
```bash
pytest  # Uses pytest.ini settings
```

**Note:** Parallel execution improves speed for large test suites. Adjust worker count based on your machine's CPU cores.

## How to View Reports

After running tests, open the HTML report:

```bash
# Open the combined report (if available)
open reports/report.html

# Or open specific suite reports
open reports/ui_report.html
open reports/api_report.html
```

Reports include:
- ✅ Test results (passed/failed/skipped)
- 📸 Screenshots for failed UI tests
- 📋 Console logs captured during execution
- ⏱️ Execution time for each test

## CI/CD Pipeline

Tests automatically run on:
- Push to `main` or `master` branches
- Pull requests
- Manual triggers via GitHub Actions

### Latest CI Run

View the latest test results: [GitHub Actions Workflow](../../actions)

**To manually trigger the workflow:**
1. Go to **Actions** tab in GitHub
2. Select **CI** workflow
3. Click **Run workflow** button

### CI Features
- Parallel execution of UI and API test suites
- Automatic artifact uploads (reports, logs, screenshots)
- Runs on Ubuntu Linux environment

## Project Structure

```
├── ui/                      # UI test files
│   └── test_client_ui.py
├── api/                     # API test files
│   └── test_posts.py
├── pages/                   # Page Object Model classes
│   ├── login_page.py
│   └── inventory_page.py
├── utils/                   # Shared utilities
│   ├── api_client.py       # HTTP client with retry logic
│   └── conftest.py         # pytest fixtures & hooks
├── config.json             # Test configuration
├── requirements.txt        # Python dependencies
├── pytest.ini              # pytest configuration
└── .github/workflows/ci.yml # GitHub Actions workflow
```

## Configuration

Edit `config.json` to customize:
- **UI Settings:** Browser type, base URL, timeouts
- **API Settings:** API base URL, request/response payloads
- **Credentials:** Test account username and password

```json
{
  "base_url": "https://example.com",
  "browser": "chromium",
  "timeout": 10000,
  "credentials": {
    "username": "user@example.com",
    "password": "password123"
  },
  "api": {
    "base_url": "https://api.example.com"
  }
}
```

## Dependencies

- **pytest** - Test framework
- **pytest-xdist** - Parallel test execution
- **pytest-html** - HTML test reports
- **playwright** - Browser automation
- **requests** - HTTP client for API tests
