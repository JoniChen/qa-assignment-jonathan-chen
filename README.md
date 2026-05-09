# UI Test Scaffold

This project uses `pytest` with Playwright for Python to login to a website and add an item to the cart.

## Setup

1. Install dependencies:

```bash
python -m pip install -r requirements.txt
```

2. Install Playwright browser binaries:

```bash
python -m playwright install
```

## Run tests

```bash
pytest
```

## Config

`config.json` contains the base URL, browser name, timeouts, and login credentials.
