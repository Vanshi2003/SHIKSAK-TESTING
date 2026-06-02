import os
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from jira import JIRA

# --- SETUP DYNAMIC REPORTING ---
issue_key = os.getenv("ISSUE_KEY", "VINT-8")
jira = JIRA(
    server="https://shiksak-team.atlassian.net",
    basic_auth=(os.getenv("JIRA_EMAIL"), os.getenv("JIRA_API_TOKEN"))
)

def log_to_jira(status, test_name, message=""):
    try:
        comment = f"Test: {test_name} | Status: {status}\nDetails: {message}"
        jira.add_comment(issue_key, comment)
    except Exception as e:
        print(f"Failed to log to Jira: {e}")

BASE_URL = "https://vintedemo.shiksak.com"

# --- BROWSER SETUP ---
@pytest.fixture
def driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new") 
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

# --- WRAPPED TEST CASES ---
def test_valid_login_flow(driver):
    test_name = "Multi-User Valid Login"
    try:
        driver.get(f"{BASE_URL}/candidate/login")
        driver.find_element(By.ID, "email").send_keys("vanshi9061@gmail.com")
        driver.find_element(By.ID, "password").send_keys("Vans@1234")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        success = WebDriverWait(driver, 10).until(EC.url_contains("/dashboard"))
        assert success == True
        log_to_jira("PASSED", test_name)
    except Exception as e:
        log_to_jira("FAILED", test_name, str(e))
        raise e

def test_invalid_login(driver):
    test_name = "Invalid Login Restriction"
    try:
        driver.get(f"{BASE_URL}/candidate/login")
        driver.find_element(By.ID, "email").send_keys("wrong_user@shiksak.com")
        driver.find_element(By.ID, "password").send_keys("WrongPassword123")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        error_popup = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'failed') or contains(text(), 'invalid')]"))
        )
        assert error_popup is not None
        log_to_jira("PASSED", test_name)
    except Exception as e:
        log_to_jira("FAILED", test_name, str(e))
        raise e

# (You can apply this exact try/except block to your other test functions as well!)
