import json
import sys
from pathlib import Path
import pytest
from playwright.sync_api import sync_playwright

ROOT_PATH = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT_PATH))
CONFIG_PATH = ROOT_PATH / "config.json"
CONSOLE_LOGS_DIR = ROOT_PATH / "console_logs"
SCREENSHOTS_DIR = ROOT_PATH / "screenshots"

# Create directories if they don't exist
CONSOLE_LOGS_DIR.mkdir(exist_ok=True)
SCREENSHOTS_DIR.mkdir(exist_ok=True)


def load_config():
    with open(CONFIG_PATH, encoding="utf-8") as config_file:
        return json.load(config_file)


@pytest.fixture(scope="function")
def config():
    return load_config()


@pytest.fixture(scope="function")
def page(config, request):
    with sync_playwright() as playwright:
        browser_type = getattr(playwright, config["browser"])
        browser = browser_type.launch(headless=False)
        context = browser.new_context(
            base_url=config["base_url"],
            viewport={"width": 1280, "height": 720},
        )
        console_logs = []

        def handle_console(msg):
            location = msg.location
            console_logs.append({
                "type": msg.type,
                "text": msg.text,
                "location": {
                    "url": location.get("url"),
                    "lineNumber": location.get("lineNumber"),
                    "columnNumber": location.get("columnNumber")
                }
            })

        page = context.new_page()
        page.on("console", handle_console)
        context.set_default_timeout(config["timeouts"]["action"])
        
        yield page
        
        test_name = request.node.name
        console_log_path = CONSOLE_LOGS_DIR / f"{test_name}.log"
        screenshot_path = SCREENSHOTS_DIR / f"{test_name}.png"

        if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
            try:
                with console_log_path.open("w", encoding="utf-8") as log_file:
                    for entry in console_logs:
                        log_file.write(f"[{entry['type']}] {entry['text']} ")
                        if entry["location"]["url"]:
                            log_file.write(f"({entry['location']['url']}:{entry['location']['lineNumber']}:{entry['location']['columnNumber']})")
                        log_file.write("\n")

                page.screenshot(path=str(screenshot_path))
            except Exception as e:
                print(f"Error capturing console log or screenshot: {e}")
        else:
            console_log_path.unlink(missing_ok=True)
            screenshot_path.unlink(missing_ok=True)

        context.close()
        browser.close()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)
