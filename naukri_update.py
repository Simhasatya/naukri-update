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

# -----------------------------
# Configuration
# -----------------------------
# Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Resume folder and list
RESUME_FOLDER = r"C:\Users\ASUS\Desktop\naukri_update\Satya_Resumes"
RESUMES = [
    "Narasimha_Rayudu.pdf",
    "Satya Aws & GCP.pdf",
    "Satya5+Cloud  DevOps.pdf"
]

# Environment variables for credentials
EMAILS = [os.getenv(f"NAUKRI_EMAIL_{i+1}") for i in range(3)]
PASSWORDS = [os.getenv(f"NAUKRI_PASSWORD_{i+1}") for i in range(3)]

# Validate credentials
for idx, (email, password) in enumerate(zip(EMAILS, PASSWORDS), start=1):
    if not email or not password:
        logging.error(f"❌ Credentials missing for account {idx}. Please set NAUKRI_EMAIL_{idx} and NAUKRI_PASSWORD_{idx}")
        exit(1)

# -----------------------------
# Function to update resume
# -----------------------------
def update_resume(email, password, resume_file, headless=True):
    resume_path = os.path.join(RESUME_FOLDER, resume_file)
    if not os.path.exists(resume_path):
        logging.error(f"❌ Resume file not found: {resume_path}")
        return

    logging.info(f"🚀 Starting update for {email} with resume {resume_file}")

    # Chrome options
    chrome_options = Options()
    if headless:
        chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument(f"--user-data-dir=/tmp/naukri_profile_{int(time.time())}")

    # Initialize Chrome driver
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
        # Open login page
        logging.info("🌐 Opening Naukri login page...")
        driver.get("https://www.naukri.com/nlogin/login")

        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, "email")))

        # Login
        logging.info("🔑 Logging in...")
        driver.find_element(By.NAME, "email").send_keys(email)
        driver.find_element(By.NAME, "password").send_keys(password)  # corrected field name
        driver.find_element(By.XPATH, "//button[text()='Login']").click()

        logging.info("⌛ Waiting for homepage to load...")
        time.sleep(10)  # Wait for login to complete

        # Navigate to profile page
        logging.info("🧭 Navigating to profile page...")
        driver.get("https://www.naukri.com/mnjuser/profile")
        time.sleep(5)

        # Upload resume
        logging.info(f"📂 Uploading resume: {resume_path}")
        upload_button = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='file']"))
        )
        upload_button.send_keys(resume_path)

        # Optional: wait for confirmation element
        time.sleep(5)

        # Take screenshot for verification
        screenshot_path = os.path.join(RESUME_FOLDER, f"{email.replace('@','_')}_upload.png")
        driver.save_screenshot(screenshot_path)
        logging.info(f"📸 Screenshot saved: {screenshot_path}")

        logging.info("✅ Resume uploaded successfully!")

    except Exception as e:
        logging.error(f"⚠️ Error during resume update for {email}: {e}")
    finally:
        driver.quit()

# -----------------------------
# Run updates for all accounts
# -----------------------------
# Set headless=False to see browser for local testing
for email, password, resume_file in zip(EMAILS, PASSWORDS, RESUMES):
    update_resume(email, password, resume_file, headless=False)
