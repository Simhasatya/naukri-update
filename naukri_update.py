import logging
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# --- Logging setup ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# --- Accounts setup ---
accounts = [
    {
        "email": os.getenv("NAUKRI_EMAIL_1"),
        "password": os.getenv("NAUKRI_PASSWORD_1"),
        "resume": "Narasimha_Rayudu.pdf",
    },
    {
        "email": os.getenv("NAUKRI_EMAIL_2"),
        "password": os.getenv("NAUKRI_PASSWORD_2"),
        "resume": "Satya Aws & GCP.pdf",
    },
    {
        "email": os.getenv("NAUKRI_EMAIL_3"),
        "password": os.getenv("NAUKRI_PASSWORD_3"),
        "resume": "Satya5+Cloud  DevOps.pdf",
    },
]

# --- Chrome options ---
options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--window-size=1920,1080")

def update_resume(account):
    resume_path = f"/home/runner/work/naukri-auto-update/naukri-auto-update/Satya_Resumes/{account['resume']}"
    logging.info(f"Starting update for {account['email']}")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    wait = WebDriverWait(driver, 30)

    try:
        driver.get("https://www.naukri.com/nlogin/login")
        time.sleep(5)
        driver.save_screenshot(f"{account['email']}_login.png")

        username = wait.until(EC.presence_of_element_located((By.ID, "usernameField")))
        password = wait.until(EC.presence_of_element_located((By.ID, "passwordField")))
        login_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Login')]")))

        username.send_keys(account["email"])
        password.send_keys(account["password"])
        login_btn.click()
        logging.info("Login clicked")

        wait.until(EC.url_contains("/homepage"))
        logging.info("Login successful")

        driver.get("https://www.naukri.com/mnjuser/profile")
        wait.until(EC.url_contains("/profile"))

        upload_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='file']")))
        driver.execute_script("arguments[0].style.display = 'block';", upload_input)
        upload_input.send_keys(resume_path)
        logging.info("Resume uploaded successfully")

        driver.save_screenshot(f"{account['email']}_success.png")

        driver.get("https://www.naukri.com/nlogout/logout")
        logging.info("Logged out")

    except Exception as e:
        logging.error(f"Error for {account['email']}: {e}")
        driver.save_screenshot(f"{account['email']}_error.png")
    finally:
        driver.quit()

for acc in accounts:
    update_resume(acc)
