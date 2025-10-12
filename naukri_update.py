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

# Logging setup
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Resume path (change only if needed)
RESUME_FOLDER = r"C:\Users\ASUS\Desktop\naukri_update\Satya_Resumes"

# Pick one resume automatically (you can rotate this logic if needed)
RESUME_FILE = "Satya5+Cloud  DevOps.pdf"
RESUME_PATH = os.path.join(RESUME_FOLDER, RESUME_FILE)

# Get credentials from environment
EMAIL = os.getenv("NAUKRI_EMAIL_1")
PASSWORD = os.getenv("NAUKRI_PASSWORD_1")

if not EMAIL or not PASSWORD:
    logging.error("❌ Naukri credentials not found in environment variables.")
    exit(1)

# Chrome setup
chrome_options = Options()
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")

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

    # Wait for page load
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.NAME, "email")))

    logging.info("🔑 Logging into Naukri account...")
    driver.find_element(By.NAME, "email").send_keys(EMAIL)
    driver.find_element(By.NAME, "password").send_keys(PASSWORD)  # ✅ fixed here
    driver.find_element(By.XPATH, "//button[text()='Login']").click()

    # Wait after login for homepage to load
    logging.info("⌛ Waiting for homepage to load...")
    time.sleep(20)  # increased for stability

    # Go to profile page
    logging.info("🧭 Navigating to profile page...")
    driver.get("https://www.naukri.com/mnjuser/profile")

    # Wait for profile page to load
    time.sleep(15)

    # Upload resume
    logging.info("📂 Uploading new resume: %s", RESUME_PATH)
    upload_button = WebDriverWait(driver, 25).until(
        EC.presence_of_element_located((By.XPATH, "//input[@type='file']"))
    )
    upload_button.send_keys(RESUME_PATH)

    logging.info("✅ Resume uploaded successfully. Waiting to ensure completion...")
    time.sleep(10)

    logging.info("🎉 Resume update complete! Closing browser.")
    driver.quit()

except Exception as e:
    logging.error(f"⚠️ Error during resume update: {e}")
    driver.quit()
