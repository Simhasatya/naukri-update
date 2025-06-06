import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Load credentials from environment variables
NAUKRI_EMAIL = os.getenv("NAUKRI_EMAIL")
NAUKRI_PASSWORD = os.getenv("NAUKRI_PASSWORD")
RESUME_PATH = os.getenv("RESUME_PATH")

# Path to the system-installed Chrome and ChromeDriver
CHROME_PATH = "/usr/bin/chromium"
CHROMEDRIVER_PATH = "/usr/bin/chromedriver"

# Setup Chrome options
options = Options()
options.binary_location = CHROME_PATH
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--proxy-server='direct://'")
options.add_argument("--proxy-bypass-list=*")

# Initialize WebDriver using system ChromeDriver
driver = webdriver.Chrome(service=Service(CHROMEDRIVER_PATH), options=options)
wait = WebDriverWait(driver, 30)

try:
    driver.get("https://www.naukri.com/mnjuser/login")
    wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Enter your active Email ID / Username']"))).send_keys(NAUKRI_EMAIL)
    wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Enter your password']"))).send_keys(NAUKRI_PASSWORD)
    wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Login')]"))).click()

    wait.until(EC.url_contains("/homepage"))
    driver.get("https://www.naukri.com/mnjuser/profile")

    upload_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='file']")))
    upload_btn.send_keys(RESUME_PATH)

    time.sleep(5)
    print("✅ Resume updated successfully.")
except Exception as e:
    print(f"❌ Error occurred: {e}")
finally:
    driver.quit()
