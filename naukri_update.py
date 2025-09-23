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
# Logging
# -----------------------
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename="logs/naukri_update.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# -----------------------
# Resume Folder
# -----------------------
RESUME_FOLDER = "Satya_Resumes"
RESUME_FILES = [
    "Narasimha_Rayudu.pdf",
    "Satya Aws & GCP.pdf",
    "Satya5+Cloud  DevOps.pdf"
]

# -----------------------
# Accounts - from secrets
# -----------------------
accounts = [
    {"email": os.getenv("NAUKRI_EMAIL_1"), "password": os.getenv("NAUKRI_PASSWORD_1")},
    {"email": os.getenv("NAUKRI_EMAIL_2"), "password": os.getenv("NAUKRI_PASSWORD_2")},
    {"email": os.getenv("NAUKRI_EMAIL_3"), "password": os.getenv("NAUKRI_PASSWORD_3")},
]

# Remove empty accounts (if any secret is missing)
accounts = [acc for acc in accounts if acc["email"] and acc["password"]]

# -----------------------
# Selenium Options
# -----------------------
options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

def update_resume(account):
    logging.info(f"Updating resume for: {account['email']}")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.set_window_size(1280, 1024)

    try:
        driver.get("https://www.naukri.com/nlogin/login")
        wait = WebDriverWait(driver, 20)

        # Login
        wait.until(EC.presence_of_element_located((By.NAME, "email"))).send_keys(account["email"])
        driver.find_element(By.NAME, "PASSWORD").send_keys(account["password"])
        driver.find_element(By.XPATH, "//button[@type='submit']").click()

        # Wait for redirect (homepage OR profile)
        wait.until(
            lambda d: "/homepage" in d.current_url or "/profile" in d.current_url,
            "Login redirect failed"
        )
        driver.save_screenshot(f"logs/{account['email']}_after_login.png")

        # Go to profile
        driver.get("https://www.naukri.com/mnjuser/profile")

        # Upload each resume
        for resume in RESUME_FILES:
            resume_path = os.path.join(RESUME_FOLDER, resume)
            if os.path.exists(resume_path):
                try:
                    upload = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='file']")))
                    upload.send_keys(os.path.abspath(resume_path))
                    time.sleep(3)
                    logging.info(f"Uploaded resume: {resume}")
                except Exception as e:
                    logging.error(f"Failed to upload {resume}: {e}")
            else:
                logging.error(f"Resume file not found: {resume_path}")

        driver.save_screenshot(f"logs/{account['email']}_after_upload.png")
        logging.info(f"Resume update completed for: {account['email']}")

    except Exception as e:
        logging.error(f"Error updating {account['email']}: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    for acc in accounts:
        update_resume(acc)
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
# Logging
# -----------------------
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename="logs/naukri_update.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# -----------------------
# Resume Folder
# -----------------------
RESUME_FOLDER = "Satya_Resumes"
RESUME_FILES = [
    "Narasimha_Rayudu.pdf",
    "Satya Aws & GCP.pdf",
    "Satya5+Cloud  DevOps.pdf"
]

# -----------------------
# Accounts - from secrets
# -----------------------
accounts = [
    {"email": os.getenv("NAUKRI_EMAIL_1"), "password": os.getenv("NAUKRI_PASSWORD_1")},
    {"email": os.getenv("NAUKRI_EMAIL_2"), "password": os.getenv("NAUKRI_PASSWORD_2")},
    {"email": os.getenv("NAUKRI_EMAIL_3"), "password": os.getenv("NAUKRI_PASSWORD_3")},
]

# Remove empty accounts (if any secret is missing)
accounts = [acc for acc in accounts if acc["email"] and acc["password"]]

# -----------------------
# Selenium Options
# -----------------------
options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

def update_resume(account):
    logging.info(f"Updating resume for: {account['email']}")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.set_window_size(1280, 1024)

    try:
        driver.get("https://www.naukri.com/nlogin/login")
        wait = WebDriverWait(driver, 20)

        # Login
        wait.until(EC.presence_of_element_located((By.NAME, "email"))).send_keys(account["email"])
        driver.find_element(By.NAME, "PASSWORD").send_keys(account["password"])
        driver.find_element(By.XPATH, "//button[@type='submit']").click()

        # Wait for redirect (homepage OR profile)
        wait.until(
            lambda d: "/homepage" in d.current_url or "/profile" in d.current_url,
            "Login redirect failed"
        )
        driver.save_screenshot(f"logs/{account['email']}_after_login.png")

        # Go to profile
        driver.get("https://www.naukri.com/mnjuser/profile")

        # Upload each resume
        for resume in RESUME_FILES:
            resume_path = os.path.join(RESUME_FOLDER, resume)
            if os.path.exists(resume_path):
                try:
                    upload = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='file']")))
                    upload.send_keys(os.path.abspath(resume_path))
                    time.sleep(3)
                    logging.info(f"Uploaded resume: {resume}")
                except Exception as e:
                    logging.error(f"Failed to upload {resume}: {e}")
            else:
                logging.error(f"Resume file not found: {resume_path}")

        driver.save_screenshot(f"logs/{account['email']}_after_upload.png")
        logging.info(f"Resume update completed for: {account['email']}")

    except Exception as e:
        logging.error(f"Error updating {account['email']}: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    for acc in accounts:
        update_resume(acc)
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
# Logging
# -----------------------
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename="logs/naukri_update.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# -----------------------
# Resume Folder
# -----------------------
RESUME_FOLDER = "Satya_Resumes"
RESUME_FILES = [
    "Narasimha_Rayudu.pdf",
    "Satya Aws & GCP.pdf",
    "Satya5+Cloud  DevOps.pdf"
]

# -----------------------
# Accounts - from secrets
# -----------------------
accounts = [
    {"email": os.getenv("NAUKRI_EMAIL_1"), "password": os.getenv("NAUKRI_PASSWORD_1")},
    {"email": os.getenv("NAUKRI_EMAIL_2"), "password": os.getenv("NAUKRI_PASSWORD_2")},
    {"email": os.getenv("NAUKRI_EMAIL_3"), "password": os.getenv("NAUKRI_PASSWORD_3")},
]

# Remove empty accounts (if any secret is missing)
accounts = [acc for acc in accounts if acc["email"] and acc["password"]]

# -----------------------
# Selenium Options
# -----------------------
options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

def update_resume(account):
    logging.info(f"Updating resume for: {account['email']}")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.set_window_size(1280, 1024)

    try:
        driver.get("https://www.naukri.com/nlogin/login")
        wait = WebDriverWait(driver, 20)

        # Login
        wait.until(EC.presence_of_element_located((By.NAME, "email"))).send_keys(account["email"])
        driver.find_element(By.NAME, "PASSWORD").send_keys(account["password"])
        driver.find_element(By.XPATH, "//button[@type='submit']").click()

        # Wait for redirect (homepage OR profile)
        wait.until(
            lambda d: "/homepage" in d.current_url or "/profile" in d.current_url,
            "Login redirect failed"
        )
        driver.save_screenshot(f"logs/{account['email']}_after_login.png")

        # Go to profile
        driver.get("https://www.naukri.com/mnjuser/profile")

        # Upload each resume
        for resume in RESUME_FILES:
            resume_path = os.path.join(RESUME_FOLDER, resume)
            if os.path.exists(resume_path):
                try:
                    upload = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='file']")))
                    upload.send_keys(os.path.abspath(resume_path))
                    time.sleep(3)
                    logging.info(f"Uploaded resume: {resume}")
                except Exception as e:
                    logging.error(f"Failed to upload {resume}: {e}")
            else:
                logging.error(f"Resume file not found: {resume_path}")

        driver.save_screenshot(f"logs/{account['email']}_after_upload.png")
        logging.info(f"Resume update completed for: {account['email']}")

    except Exception as e:
        logging.error(f"Error updating {account['email']}: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    for acc in accounts:
        update_resume(acc)
