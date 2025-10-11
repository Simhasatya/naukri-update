import pickle
import time
import os
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium_stealth import stealth

# ==============================
# Resume folder
# ==============================
resume_folder = "Satya_Resumes"

# ==============================
# Screenshots folder
# ==============================
os.makedirs("screenshots", exist_ok=True)

# ==============================
# Chrome setup (headless + stealth)
# ==============================
options = Options()
options.add_argument("--headless=new")
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

def update_resume(account):
    resume_path = os.path.join(resume_folder, account["resume"])
    if not os.path.exists(resume_path):
        print(f"❌ Resume not found for {account['email']}: {resume_path}")
        return

    print(f"\n🚀 Starting update for {account['email']} with resume {account['resume']}")

    driver = webdriver.Chrome(service=Service(), options=options)

    # Apply stealth mode
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
        driver.get("https://www.naukri.com/")

        # Load cookies (saved from manual login)
        with open("cookies.pkl", "rb") as f:
            cookies = pickle.load(f)

        for cookie in cookies:
            cookie.pop("expiry", None)  # remove expiry to avoid errors
            driver.add_cookie(cookie)

        driver.refresh()
        time.sleep(5)
        print("✅ Logged in using saved cookies (no OTP).")

        # Navigate to profile page
        driver.get("https://www.naukri.com/mnjuser/profile")
        time.sleep(5)

        # Upload resume
        upload_input = driver.find_element("xpath", "//input[@type='file']")
        driver.execute_script("arguments[0].style.display = 'block';", upload_input)
        upload_input.send_keys(resume_path)
        print(f"✅ Resume uploaded successfully for {account['email']}")

        time.sleep(5)

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
