import os
import pytest
from selenium import webdriver
from pytest_html import extras

# ensure reports folder exists
os.makedirs("reports", exist_ok=True)

# ✅ FIX: Add this fixture
@pytest.fixture(scope="function")
def setup():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get("https://the-internet.herokuapp.com/login")
    yield driver
    driver.quit()

# ✅ Report + Screenshot hook
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call":
        extra = getattr(rep, "extra", [])

        # Add username/password
        test_data = item.funcargs.get("test_data", None)
        if test_data:
            extra.append(extras.text(f"Username: {test_data.get('username')}"))
            extra.append(extras.text(f"Password: {test_data.get('password')}"))

        # Screenshot on failure
        if rep.failed:
            driver = item.funcargs.get("setup", None)
            if driver:
                file_name = f"reports/{item.name}.png"
                driver.save_screenshot(file_name)
                extra.append(extras.image(file_name))

        rep.extra = extra