import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium_stealth import stealth

# -----------------------
# Logging setup
# -----------------------
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# -----------------------
# Resume path
# -----------------------
RESUME_FOLDER = r"C:\Users\ASUS\Desktop\naukri_update\Satya_Resumes"  # Update if needed
RESUME_FILE = "Satya5+Cloud  DevOps.pdf"  # Choose resume to upload
RESUME_PATH = os.path.join(RESUME_FOLDER, RESUME_FILE)

# -----------------------
# Credentials from environment variables
# -----------------------
EMAIL = os.getenv("NAUKRI_EMAIL_1")
PASSWORD = os.getenv("NAUKRI_PASSWORD_1")

if not EMAIL or not PASSWORD:
    logging.error("❌ Naukri credentials not found in environment variables.")
    exit(1)

# -----------------------
# Chrome setup for headless CI
# -----------------------
chrome_options = Options()
chrome_options.add_argument("--headless=new")  # headless mode for GitHub Actions
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument(f"--user-data-dir=/tmp/chrome_userdata_{int(time.time())}")

service = Service()
driver = webdriver.Chrome(service=service, options=chrome_options)

# Stealth to avoid detection
stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True)

# -----------------------
# Resume upload automation
# -----------------------
try:
    logging.info("🌐 Opening Naukri login page...")
    driver.get("https://www.naukri.com/nlogin/login")

    # Wait for login fields
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.NAME, "email")))

    logging.info("🔑 Logging into Naukri account...")
    driver.find_element(By.NAME, "email").send_keys(EMAIL)
    driver.find_element(By.NAME, "PASSWORD").send_keys(PASSWORD)
    driver.find_element(By.XPATH, "//button[text()='Login']").click()

    # Wait for homepage to load
    logging.info("⌛ Waiting for homepage to load...")
    time.sleep(10)

    # Navigate to profile page
    logging.info("🧭 Navigating to profile page...")
    driver.get("https://www.naukri.com/mnjuser/profile")
    time.sleep(5)

    # Upload resume
    logging.info("📂 Uploading new resume: %s", RESUME_PATH)
    upload_button = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//input[@type='file']"))
    )
    upload_button.send_keys(RESUME_PATH)
    time.sleep(10)  # Wait to ensure upload completes

    logging.info("✅ Resume uploaded successfully!")
    driver.quit()

except Exception as e:
    logging.error(f"⚠️ Error during resume update: {e}")
    driver.quit()
