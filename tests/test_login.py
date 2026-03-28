import pytest
from pages.login_page import LoginPage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

def wait_for_message(driver):
    wait = WebDriverWait(driver, 10)
    return wait.until(EC.visibility_of_element_located((By.ID, "flash")))

@pytest.mark.parametrize(
    "test_data",
    [
        {
            "username": "tomsmith",
            "password": "SuperSecretPassword!",
            "expected": "secure area"
        },
        {
            "username": "wrong",
            "password": "wrong",
            "expected": "invalid"
        }
    ],
    ids=lambda x: f"{x['username']}-{x['password']}"
)
def test_login(setup, test_data):
    driver = setup
    login = LoginPage(driver)


    login.enter_username(test_data["username"])
    login.enter_password(test_data["password"])
    login.click_login()

    # ✅ Clean message properly
    message = wait_for_message(driver).text
    message = message.lower().replace("×", "").strip()

    print("Result:", message)

    time.sleep(3)

    # ✅ Correct assertion
    assert "secure area" in message,\
        f"Expected: {test_data['expected']}, Got: {message}"
    