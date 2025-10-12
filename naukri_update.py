import os
import re
import time
import logging
import pickle
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium_stealth import stealth

logging.basicConfig(level=logging.INFO, format="%(message)s")

# -------------------------------
# SETUP
# -------------------------------
RESUME_DIR = r"C:\Users\ASUS\Desktop\naukri_update\Satya_Resumes"
RESUMES = {
    "simhasatya970@gmail.com": os.path.join(RESUME_DIR, "Narasimha_Rayudu.pdf"),
    "satyacloud59@gmail.com": os.path.join(RESUME_DIR, "Satya Aws & GCP.pdf"),
    "satyadevops@gmail.com": os.path.join(RESUME_DIR, "Satya5+Cloud  DevOps.pdf"),
}

accounts = [
    {"email": os.getenv("NAUKRI_EMAIL_1"), "password": os.getenv("NAUKRI_PASSWORD_1")},
    {"email": os.getenv("NAUKRI_EMAIL_2"), "password": os.getenv("NAUKRI_PASSWORD_2")},
]

# Remove empty accounts
accounts = [acc for acc in accounts if acc["email"] and acc["password"]]


def sanitize_filename(name):
    """Clean email for filename use."""
    return re.sub(r"[^a-zA-Z0-9_-]", "_", name)


def setup_driver():
    """Initialize Chrome WebDriver in normal (visible) mode."""
    options = Options()
    options.add_argument("--start-maximized")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    driver = webdriver.Chrome(options=options)
    stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True)
    return driver


def update_resume(account):
    """Logs in and uploads resume on Naukri."""
    email = account["email"]
    password = account["password"]
    resume_path = RESUMES.get(email)

    if not os.path.exists(resume_path):
        logging.error(f"❌ Resume not found: {resume_path}")
        return

    logging.info(f"\n🚀 Starting update for {email} with resume {os.path.basename(resume_path)}")

    driver = setup_driver()

    try:
        driver.get("https://www.naukri.com/nlogin/login")

        # Login
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "usernameField"))).send_keys(email)
        driver.find_element(By.ID, "passwordField").send_keys(password)
        driver.find_element(By.XPATH, "//button[contains(text(),'Login')]").click()

        logging.info("🔹 If OTP is requested, please complete login manually and press Enter here once on dashboard...")
        input()  # Wait for manual OTP if required

        # Wait for profile to load
        WebDriverWait(driver, 60).until(EC.url_contains("naukri.com/mnjuser"))
        logging.info("✅ Logged in successfully.")

        driver.get("https://www.naukri.com/mnjuser/profile")
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        logging.info("✅ Profile page loaded.")

        # Upload resume
        upload_input = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='file' and @id='attachCV']"))
        )
        upload_input.send_keys(resume_path)
        logging.info(f"✅ Resume uploaded successfully: {resume_path}")

        time.sleep(5)  # Wait for upload confirmation
        logging.info("✅ Resume update complete!")

    except Exception as e:
        safe_email = sanitize_filename(email)
        screenshot_path = f"screenshots/{safe_email}_error.png"
        os.makedirs("screenshots", exist_ok=True)
        driver.save_screenshot(screenshot_path)
        logging.error(f"❌ Error for {email}: {e}")
        logging.info(f"📸 Screenshot saved: {screenshot_path}")

    finally:
        time.sleep(3)
        driver.quit()


if __name__ == "__main__":
    for acc in accounts:
        update_resume(acc)
