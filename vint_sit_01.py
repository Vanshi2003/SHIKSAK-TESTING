import os
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from jira import JIRA # Added Jira library

# 1. SETUP DYNAMIC REPORTING
issue_key = os.getenv("ISSUE_KEY", "VINT-8") # Falls back to VINT-8 if no key is passed
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

# 2. BROWSER SETUP (HEADLESS FOR GITHUB)
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

# 3. EXAMPLE OF WRAPPED TEST CASE
# Apply this pattern to your other tests
def test_valid_login_flow(driver):
    test_name = "Multi-User Valid Login"
    try:
        # ... your existing login logic ...
        # (Assuming your logic runs here)
        log_to_jira("PASSED", test_name)
    except Exception as e:
        log_to_jira("FAILED", test_name, str(e))
        raise e
