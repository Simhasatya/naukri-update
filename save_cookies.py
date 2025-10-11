from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pickle
import time

options = Options()
# Comment out headless mode
# options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")

driver = webdriver.Chrome(options=options)
driver.get("https://www.naukri.com/nlogin")

input("🔹 Please log in manually (enter OTP if asked). Press Enter once you’re on dashboard...")

# Wait a few seconds to ensure cookies are loaded
time.sleep(3)

# Save cookies
with open("cookies.pkl", "wb") as f:
    pickle.dump(driver.get_cookies(), f)

print("✅ Cookies saved successfully as cookies.pkl")
driver.quit()
