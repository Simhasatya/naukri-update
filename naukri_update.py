from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium_stealth import stealth
import time
import os
import re

# ==============================
# Resume folder
# ==============================
resume_folder = "Satya_Resumes"

# ==============================
# Screenshots folder
# ==============================
os.makedirs("screenshots", exist_ok=True)

# ==============================
# Chrome setup (visible mode)
# ==============================
options = webdriver.ChromeOptions()
# Remove headless so you can see Chrome
# options.add_argument("--headless=new")  # Commented out
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--window-size=1920,1080")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--disable-gpu")
options.add_argument(
    "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/119.0.6045.123 Safari/537.36"
)

# ==============================
# Accounts list with dedicated resumes
# ==============================
accounts = [
    {
        "email": os.environ.get("NAUKRI_EMAIL_1"),
        "password": os.environ.get("NAUKRI_PASSWORD_1"),
        "resume": "Narasimha_Rayudu.pdf"
    },
    {
        "email": os.environ.get("NAUKRI_EMAIL_2"),
        "password": os.environ.get("NAUKRI_PASSWORD_2"),
        "resume": "Satya Aws & GCP.pdf"
    },
    {
        "email": os.environ.get("NAUKRI_EMAIL_3"),
        "password": os.environ.get("NAUKRI_PASSWORD_3"),
        "resume": "Satya5+Cloud  DevOps.pdf"
    }
]

def sanitize_filename(name):
    return re.sub(r'[^a-zA-Z0-9_-]', '_', name)

def update_resume(account):
    resume_path = os.path.join(resume_folder, account["resume"])
    if not os.path.exists(resume_path):
        print(f"❌ Resume not found for {account['email']}: {resume_path}")
        return

    print(f"\n🚀 Starting update for {account['email']} with resume {account['resume']}")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    wait = WebDriverWait(driver, 60)

    # Apply stealth mode to mask Selenium
    stealth(
        driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
    )

    try:
        # Navigate to login page
        driver.get("https://www.naukri.com/nlogin/login")
        time.sleep(5)  # wait to see page

        # Username field
        username = wait.until(EC.presence_of_element_located((By.ID, "usernameField")))
        username.click()
        username.clear()
        username.send_keys(account["email"])

        # Password field
        password = wait.until(EC.presence_of_element_located((By.ID, "passwordField")))
        time.sleep(2)  # wait for rendering
        password.click()
        password.clear()
        password.send_keys(account["password"])

        # Click Login
        login_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Login')]")))
        login_btn.click()

        # Wait for dashboard
        input("🔹 If OTP is requested, please complete login manually and press Enter here once on dashboard...")

        print("✅ Logged in successfully.")

        # Navigate to profile page
        driver.get("https://www.naukri.com/mnjuser/profile")
        wait.until(EC.url_contains("/profile"))
        print("✅ Profile page loaded.")
        time.sleep(5)  # wait to see page fully

        # Upload resume
        upload_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='file']")))
        driver.execute_script("arguments[0].style.display = 'block';", upload_input)
        upload_input.send_keys(resume_path)
        print(f"✅ Resume uploaded successfully for {account['email']}")
        time.sleep(5)  # wait to confirm upload

        # Logout
        driver.get("https://www.naukri.com/nlogout/logout")
        print(f"👋 Logged out {account['email']}")

    except Exception as e:
        print(f"❌ Error for {account['email']}: {e}")
        safe_email = sanitize_filename(account['email'])
        driver.save_screenshot(f"screenshots/{safe_email}_error.png")
        print(f"📸 Screenshot saved: screenshots/{safe_email}_error.png")

    finally:
        driver.quit()

# Run for all accounts
for acc in accounts:
    update_resume(acc)

print("\n🎉 All accounts updated successfully!")
