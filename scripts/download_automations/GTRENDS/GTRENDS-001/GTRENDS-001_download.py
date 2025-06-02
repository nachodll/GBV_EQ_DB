import os
import time
from datetime import datetime
from urllib.parse import quote

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Settings
driver_path = "/opt/homebrew/bin/chromedriver"
max_retries = 3

# Log
log_dir = os.path.join(os.path.dirname(__file__), "log")
os.makedirs(log_dir, exist_ok=True)
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
log_path = os.path.join(log_dir, f"log{timestamp}.log")
log_file = open(log_path, mode="w", encoding="utf-8")

# List of terms to be consulted
terms = ["pornhub", "xvideos"]

# Comunidades Autónomas and its codes
regions = {
    "Andalucía": "ES-AN",
    "Aragón": "ES-AR",
    "Asturias": "ES-AS",
    "Islas Baleares": "ES-IB",
    "Canarias": "ES-CN",
    "Cantabria": "ES-CB",
    "Castilla-La Mancha": "ES-CM",
    "Castilla y León": "ES-CL",
    "Cataluña": "ES-CT",
    "Comunidad Valenciana": "ES-VC",
    "Extremadura": "ES-EX",
    "Galicia": "ES-GA",
    "Madrid": "ES-MD",
    "Murcia": "ES-MC",
    "Navarra": "ES-NC",
    "País Vasco": "ES-PV",
    "La Rioja": "ES-RI",
}

# Selenium Config
options = Options()
options.add_argument("--start-maximized")
# options.add_argument("--headless")  # Activar si no necesitas ver el navegador
service = Service(driver_path)
driver = webdriver.Chrome(service=service, options=options)
wait = WebDriverWait(driver, 15)

try:
    for term in terms:
        for region_name, region_code in regions.items():
            attemp = 0
            success = False
            while attemp < max_retries and not success:
                attemp += 1
                timestamp = datetime.now().isoformat()
                print(f"🔁 Attemp {attemp}: Popularity of '{term}' in {region_name}")
                url = (
                    f"https://trends.google.com/trends/explore"
                    f"?date=all,all&geo=ES,{region_code}"
                    f"&q={quote('google')},{quote(term)}"
                    f"&hl=es"
                )

                try:
                    driver.get(url)

                    # Wait and click on export button
                    xpath = (
                        "//div[.//div[text()[contains(., 'Interés a lo largo del')]]]"
                        "//button[@class='widget-actions-item export' and @title='CSV']"
                    )
                    export_button = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
                    export_button.click()
                    print(f"✅ Download successful: {term} / {region_name}")
                    log_file.write(f"{datetime.now().isoformat()}\tSUCCESS\tDownloaded [{term}/{region_name}]\n")
                    time.sleep(1)
                    success = True

                except Exception as e:
                    msg = f"Attemp {attemp} failed: {type(e).__name__} - {str(e)}"
                    print(f"⚠️ {msg}")
                    if attemp == max_retries:
                        print(f"❌ Downloaded failed for {term} / {region_name}")
                        log_file.write(
                            f"{datetime.now().isoformat()}\tERROR\tDownload failed for [{term}/{region_name}]\n"
                        )
                    else:
                        log_file.write(
                            f"{datetime.now().isoformat()}\tWARNING\tAttemp {attemp} failed for [{term}/{region_name}]\n"  # noqa: E501
                        )
                        time.sleep(1)
finally:
    driver.quit()
    log_file.close()
    print(f"\n✅ Process finished. Log at: {log_path}")
