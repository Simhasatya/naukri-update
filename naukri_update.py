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
# Resume folder (relative in repo)
# -----------------------
resume_folder = "Satya_Resumes"
if not os.path.exists(resume_folder):
    logger.error(f"Resume folder not found: {resume_folder}")
    exit(1)
logger.info(f"Using resume folder: {resume_folder}")

# -----------------------
# Chrome options for headless mode
# -----------------------
options = webdriver.ChromeOptions()
options.add_argument("--headless=new")            # headless Chrome
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")
options.add_argument("--disable-notifications")

# -----------------------
# Accounts and dedicated resumes
# -----------------------
accounts = [
    {"email": "simhasatya970@gmail.com", "password": "Passwords@123.", "resume": "Narasimha_Rayudu.pdf"},
    {"email": "satyacloud59@gmail.com",   "password": "Passwords@123.", "resume": "Satya Aws & GCP.pdf"},
    {"email": "simhasatya3838@gmail.com", "password": "Passwords@123.", "resume": "Satya5+Cloud  DevOps.pdf"},
]

# Override from environment variables (GitHub Secrets)
for i, acct in enumerate(accounts, start=1):
    e = os.environ.get(f"NAUKRI_EMAIL_{i}")
    p = os.environ.get(f"NAUKRI_PASSWORD_{i}")
    if e:
        acct["email"] = e
    if p:
        acct["password"] = p

# -----------------------
# Function to update resume
# -----------------------
def update_resume(account):
    resume_path = os.path.join(resume_folder, account["resume"])
    if not os.path.exists(resume_path):
        logger.error(f"Resume not found for {account['email']}: {resume_path}")
        return

    logger.info(f"Starting update for {account['email']} using {account['resume']}")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    wait = WebDriverWait(driver, 30)

    try:
        driver.get("https://www.naukri.com/nlogin/login")
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
        try:
            login_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Login')]")))
        except:
            login_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@type='submit']")))
        login_btn.click()

        wait.until(EC.url_contains("/homepage"), timeout=20)
        logger.info(f"Logged in: {account['email']}")

        # Navigate to profile page
        driver.get("https://www.naukri.com/mnjuser/profile")
        wait.until(EC.url_contains("/profile"), timeout=20)
        time.sleep(3)

        # Upload resume
        upload_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='file']")))
        driver.execute_script("arguments[0].style.display = 'block';", upload_input)
        upload_input.send_keys(resume_path)
        logger.info(f"Uploaded resume for {account['email']} -> {account['resume']}")

        time.sleep(4)

        # Logout
        driver.get("https://www.naukri.com/nlogout/logout")
        logger.info(f"Logged out: {account['email']}")

    except Exception as exc:
        logger.error(f"Error updating {account['email']}: {exc}")
    finally:
        driver.quit()
        time.sleep(3)

# -----------------------
# Run all accounts
# -----------------------
if __name__ == "__main__":
    for acc in accounts:
        update_resume(acc)
    logger.info("All accounts updated successfully!")
