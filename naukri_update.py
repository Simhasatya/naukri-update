import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# -----------------------
# Logging setup
# -----------------------
if not os.path.exists("logs"):
    os.makedirs("logs")

logging.basicConfig(
    filename="logs/naukri_update.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
logger.addHandler(console_handler)

# -----------------------
# Resume folder
# -----------------------
resume_folder = "Satya_Resumes"
if not os.path.exists(resume_folder):
    logger.error(f"Resume folder not found: {resume_folder}")
    exit(1)

# -----------------------
# Chrome options
# -----------------------
options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")
options.add_argument("--disable-notifications")

# -----------------------
# One test account
# -----------------------
account = {
    "email": os.environ.get("NAUKRI_EMAIL_1", "simhasatya970@gmail.com"),
    "password": os.environ.get("NAUKRI_PASSWORD_1", "Passwords@123."),
    "resume": "Narasimha_Rayudu.pdf"
}

# -----------------------
# Function to update resume
# -----------------------
def update_resume(account):
    resume_path = os.path.join(resume_folder, account["resume"])
    if not os.path.exists(resume_path):
        logger.error(f"Resume not found: {resume_path}")
        return

    logger.info(f"Starting update for {account['email']}")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    wait = WebDriverWait(driver, 30)

    try:
        driver.get("https://www.naukri.com/nlogin/login")
        logger.info("Opened login page")
        time.sleep(2)

        # Enter username
        username = wait.until(EC.presence_of_element_located((By.ID, "usernameField")))
        username.clear()
        username.send_keys(account["email"])

        # Enter password
        password = wait.until(EC.presence_of_element_located((By.ID, "passwordField")))
        password.clear()
        password.send_keys(account["password"])

        # Click login
        login_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Login')]")))
        login_btn.click()

        wait.until(EC.url_contains("/homepage"))
        logger.info("Logged in successfully")

        # Navigate to profile page
        driver.get("https://www.naukri.com/mnjuser/profile")
        wait.until(EC.url_contains("/profile"))
        time.sleep(3)

        # Upload resume
        upload_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='file']")))
        driver.execute_script("arguments[0].style.display = 'block';", upload_input)
        upload_input.send_keys(resume_path)
        logger.info(f"Uploaded resume: {resume_path}")

        time.sleep(4)

        # Save screenshot for debug
        driver.save_screenshot("logs/success.png")

        # Logout
        driver.get("https://www.naukri.com/nlogout/logout")
        logger.info("Logged out")

    except Exception as exc:
        logger.error(f"Error: {exc}")
        driver.save_screenshot("logs/error.png")
    finally:
        driver.quit()

# -----------------------
# Run test
# -----------------------
if __name__ == "__main__":
    update_resume(account)
    logger.info("Test finished")
