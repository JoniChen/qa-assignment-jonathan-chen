import json
import sys
from pathlib import Path
import pytest
from playwright.sync_api import sync_playwright

ROOT_PATH = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT_PATH))
CONFIG_PATH = ROOT_PATH / "config.json"


def load_config():
    with open(CONFIG_PATH, encoding="utf-8") as config_file:
        return json.load(config_file)


@pytest.fixture(scope="function")
def config():
    return load_config()


@pytest.fixture(scope="function")
def page(config):
    with sync_playwright() as playwright:
        browser_type = getattr(playwright, config["browser"])
        browser = browser_type.launch(headless=False)
        context = browser.new_context(
            base_url=config["base_url"],
            viewport={"width": 1280, "height": 720},
        )
        context.set_default_timeout(config["timeouts"]["action"])
        page = context.new_page()
        yield page
        context.close()
        browser.close()
