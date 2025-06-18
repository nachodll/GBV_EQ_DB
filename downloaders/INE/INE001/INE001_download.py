import os
import time
from datetime import datetime
from pathlib import Path

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Settings
DRIVER_PATH = Path("/opt/homebrew/bin/chromedriver")

# Log
log_dir = os.path.join(os.path.dirname(__file__), "log")
os.makedirs(log_dir, exist_ok=True)
timestamp = datetime.now().isoformat()
log_path = os.path.join(log_dir, f"log{timestamp}.log")
log_file = open(log_path, mode="w", encoding="utf-8")

# Selenium Config
options = Options()
options.add_argument("--start-maximized")
# options.add_argument("--headless")
service = Service(str(DRIVER_PATH))
driver = webdriver.Chrome(service=service, options=options)
wait = WebDriverWait(driver, 15)

try:
    # URL
    url = "https://www.ine.es/dynt3/inebase/index.htm?padre=525#"
    driver.get(url)

    # Wait untili download buttons are loaded
    try:
        wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a[title='Formatos de descarga disponibles']"))
        )
        print("📄 Download buttons were found")
    except TimeoutException:
        print("❌ Download buttons not found")
        log_file.write(f"{datetime.now().isoformat()}\tERROR\tDownload buttons not found\n")
        driver.quit()
        exit()

    # Find download buttons
    download_buttons = driver.find_elements(By.CSS_SELECTOR, "a[title='Formatos de descarga disponibles']")
    print(f"🔎 Found {len(download_buttons)} download buttons")

    for button in download_buttons:
        try:
            provincia_elem = button.find_element(By.XPATH, ".//ancestor::li//a[contains(@class, 'titulo')]")
            provincia = provincia_elem.text.strip()
            print(f"\n➡️ Processing {provincia}")

            # Get direct link to pop up window
            popup_link = button.get_attribute("href")
            driver.execute_script("window.open(arguments[0]);", popup_link)
            driver.switch_to.window(driver.window_handles[-1])

            # Wait until pop up with file formats loads
            wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "ul.export li a")))
            formats = driver.find_elements(By.CSS_SELECTOR, "ul.export li a")
            csv_format = None
            for format in formats:
                if "CSV: separado por tabuladores" in format.get_attribute("title"):
                    csv_format = format
                    break

            if csv_format:
                href_csv = csv_format.get_attribute("href")
                driver.get(href_csv)
                print(f"⬇️ Downloading CSV for {provincia}")
                log_file.write(f"{datetime.now().isoformat()}\tSUCCESS\tDownloaded {provincia}\n")
                time.sleep(2)
            else:
                print(f"⚠️ CSV format was not found for {provincia}")
                log_file.write(f"{datetime.now().isoformat()}\tERROE\tCSV not found for {provincia}\n")

            driver.close()
            driver.switch_to.window(driver.window_handles[0])

        except Exception as e:
            print(f"❌ Error processing {provincia}: {e}")
            log_file.write(f"{datetime.now().isoformat()}\tERROR\t{str(e)}\n")
finally:
    driver.quit()
    log_file.close()
    print(f"\n✅ Process finished. Log at: {log_path}")
