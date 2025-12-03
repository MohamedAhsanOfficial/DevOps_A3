import os
import sys
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


APP_URL = os.getenv("APP_URL", "http://127.0.0.1:5000")

def build_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    # Use container-provided Chrome binary when available
    chrome_bin = os.getenv("CHROME_BIN")
    if chrome_bin:
        options.binary_location = chrome_bin

    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


def expect_contains(driver, query):
    body = driver.find_element(By.TAG_NAME, "body")
    assert query in body.text, f"Expected {query!r} on page"


def test_homepage(driver):
    driver.get(APP_URL)
    expect_contains(driver, "Capture a quick note")
    expect_contains(driver, "Add a new entry")


def test_note_submission(driver):
    driver.get(APP_URL)
    timestamp = str(int(time.time()))
    driver.find_element(By.ID, "title").send_keys(f"Note {timestamp}")
    driver.find_element(By.ID, "body").send_keys("Automated Selenium note")
    driver.find_element(By.CSS_SELECTOR, "form button").click()
    time.sleep(1)
    expect_contains(driver, "Note saved")
    expect_contains(driver, f"Note {timestamp}")


def main() -> int:
    driver = build_driver()
    try:
        test_homepage(driver)
        test_note_submission(driver)
    finally:
        driver.quit()
    print("Selenium smoke tests passed against", APP_URL)
    return 0


if __name__ == "__main__":
    sys.exit(main())
