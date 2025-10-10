import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# ==============================
# Resume folder
# ==============================
resume_folder = os.path.join(os.getcwd(), "Satya_Resumes")
screenshots_folder = os.path.join(os.getcwd(), "screenshots")
os.makedirs(screenshots_folder, exist_ok=True)

# ==============================
# Chrome setup
# ==============================
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Headless mode for GitHub Actions
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--window-size=1920,1080")

# ==============================
# Accounts list
# ==============================
accounts = [
    {
        "email": os.getenv("NAUKRI_EMAIL_1"),
        "password": os.getenv("NAUKRI_PASSWORD_1"),
        "resume": "Narasimha_Rayudu.pdf"
    },
    {
        "email": os.getenv("NAUKRI_EMAIL_2"),
        "password": os.getenv("NAUKRI_PASSWORD_2"),
        "resume": "Satya Aws & GCP.pdf"
    },
    {
        "email": os.getenv("NAUKRI_EMAIL_3"),
        "password": os.getenv("NAUKRI_PASSWORD_3"),
        "resume": "Satya5+Cloud  DevOps.pdf"
    }
]

def update_resume(account):
    resume_path = os.path.join(resume_folder, account["resume"])
    if not os.path.exists(resume_path):
        print(f"❌ Resume not found for {account['email']}: {resume_path}")
        return

    print(f"\n🚀 Starting update for {account['email']}")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    wait = WebDriverWait(driver, 30)

    try:
        # Login
        driver.get("https://www.naukri.com/nlogin/login")
        time.sleep(3)
        driver.save_screenshot(os.path.join(screenshots_folder, f"{account['email']}_login_page.png"))

        username = wait.until(EC.presence_of_element_located((By.ID, "usernameField")))
        password = wait.until(EC.presence_of_element_located((By.ID, "passwordField")))
        login_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Login')]")))

        username.send_keys(account["email"])
        password.send_keys(account["password"])
        login_btn.click()
        time.sleep(5)
        driver.save_screenshot(os.path.join(screenshots_folder, f"{account['email']}_after_login.png"))

        # Profile page
        driver.get("https://www.naukri.com/mnjuser/profile")
        time.sleep(5)
        driver.save_screenshot(os.path.join(screenshots_folder, f"{account['email']}_profile.png"))

        # Upload resume
        upload_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='file']")))
        driver.execute_script("arguments[0].style.display = 'block';", upload_input)
        upload_input.send_keys(resume_path)
        time.sleep(5)
        driver.save_screenshot(os.path.join(screenshots_folder, f"{account['email']}_resume_uploaded.png"))

        # Logout
        driver.get("https://www.naukri.com/nlogout/logout")
        driver.save_screenshot(os.path.join(screenshots_folder, f"{account['email']}_logged_out.png"))
        print(f"✅ Completed update for {account['email']}")

    except Exception as e:
        driver.save_screenshot(os.path.join(screenshots_folder, f"{account['email']}_error.png"))
        print(f"❌ Error for {account['email']}: {e}")

    finally:
        driver.quit()


for acc in accounts:
    update_resume(acc)

print("\n🎉 All accounts processed. Screenshots available in 'screenshots/' folder.")
s