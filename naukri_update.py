from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium_stealth import stealth
from webdriver_manager.chrome import ChromeDriverManager
import pickle
import os
import re
import time
import base64

# ==============================
# Resume folder
# ==============================
resume_folder = "Satya_Resumes"

# ==============================
# Screenshots folder
# ==============================
os.makedirs("screenshots", exist_ok=True)

# ==============================
# Chrome setup (stealth mode)
# ==============================
options = webdriver.ChromeOptions()
options.add_argument("--headless=new")  # headless mode for GitHub Actions
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
# Accounts list
# ==============================
accounts = [
    {
        "email": os.environ.get("NAUKRI_EMAIL_1"),
        "resume": "Narasimha_Rayudu.pdf"
    },
    {
        "email": os.environ.get("NAUKRI_EMAIL_2"),
        "resume": "Satya Aws & GCP.pdf"
    },
    {
        "email": os.environ.get("NAUKRI_EMAIL_3"),
        "resume": "Satya5+Cloud  DevOps.pdf"
    }
]

def sanitize_filename(name):
    return re.sub(r'[^a-zA-Z0-9_-]', '_', name)

def load_cookies(driver, cookie_secret):
    # Decode Base64 from GitHub secret
    cookies_bytes = base64.b64decode(cookie_secret)
    cookies = pickle.loads(cookies_bytes)
    for cookie in cookies:
        cookie.pop("expiry", None)  # prevent expired cookie errors
        driver.add_cookie(cookie)
    driver.get("https://www.naukri.com/")  # refresh after adding cookies
    time.sleep(5)

def update_resume(account):
    resume_path = os.path.join(resume_folder, account["resume"])
    if not os.path.exists(resume_path):
        print(f"❌ Resume not found for {account['email']}: {resume_path}")
        return

    print(f"\n🚀 Starting update for {account['email']} with resume {account['resume']}")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    wait = WebDriverWait(driver, 30)

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
        # Load cookies from secret
        cookie_secret = os.environ.get("NAUKRI_COOKIES")
        if not cookie_secret:
            raise Exception("NAUKRI_COOKIES secret not found!")
        load_cookies(driver, cookie_secret)

        # Navigate to profile page via link to avoid HTTP2 error
        profile_link = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//a[contains(@href,'/mnjuser/profile')]")
        ))
        profile_link.click()
        wait.until(EC.url_contains("/profile"))
        print("✅ Profile page loaded.")

        # Upload resume
        upload_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='file']")))
        driver.execute_script("arguments[0].style.display = 'block';", upload_input)
        upload_input.send_keys(resume_path)
        print(f"✅ Resume uploaded successfully for {account['email']}")
        time.sleep(5)

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
