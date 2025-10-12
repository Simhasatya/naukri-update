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

# -------------------- Logging Setup --------------------
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# -------------------- Resume Setup --------------------
RESUME_FOLDER = "./Satya_Resumes"  # relative path in repo
RESUME_FILES = [
    "Narasimha_Rayudu.pdf",
    "Satya Aws & GCP.pdf",
    "Satya5+Cloud DevOps.pdf"
]

# Pick the first resume for update (you can rotate this if needed)
RESUME_FILE = RESUME_FILES[0]
RESUME_PATH = os.path.abspath(os.path.join(RESUME_FOLDER, RESUME_FILE))

if not os.path.exists(RESUME_PATH):
    logging.error(f"❌ Resume file not found: {RESUME_PATH}")
    exit(1)

# -------------------- Credentials Setup --------------------
EMAIL = os.getenv("NAUKRI_EMAIL_1")
PASSWORD = os.getenv("NAUKRI_PASSWORD_1")

if not EMAIL or not PASSWORD:
    logging.error("❌ Naukri credentials not found in environment variables.")
    exit(1)

# -------------------- Chrome Setup --------------------
chrome_options = Options()
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

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

try:
    logging.info("🌐 Opening Naukri login page...")
    driver.get("https://www.naukri.com/nlogin/login")

    # Wait for login page to load
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.NAME, "email")))

    logging.info("🔑 Logging in...")
    driver.find_element(By.NAME, "email").send_keys(EMAIL)
    driver.find_element(By.NAME, "PASSWORD").send_keys(PASSWORD)
    driver.find_element(By.XPATH, "//button[text()='Login']").click()

    # Wait for homepage to load
    logging.info("⌛ Waiting for homepage to load...")
    time.sleep(15)

    # Navigate to profile page
    logging.info("🧭 Navigating to profile page...")
    driver.get("https://www.naukri.com/mnjuser/profile")
    time.sleep(10)

    # Upload resume
    logging.info(f"📂 Uploading resume: {RESUME_PATH}")
    upload_button = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//input[@type='file']"))
    )
    upload_button.send_keys(RESUME_PATH)

    logging.info("✅ Resume uploaded successfully. Waiting for confirmation...")
    time.sleep(10)

    logging.info("🎉 Resume update complete! Closing browser.")
    driver.quit()

except Exception as e:
    logging.error(f"⚠️ Error during resume update: {e}")
    driver.quit()
