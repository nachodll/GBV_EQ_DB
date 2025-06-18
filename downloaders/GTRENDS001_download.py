"""Fetch Google Trends popularity data using Selenium."""

import logging
import time
from datetime import datetime
from pathlib import Path
from urllib.parse import quote

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

DRIVER_PATH = Path("/opt/homebrew/bin/chromedriver")
TERMS = ["pornhub", "xvideos"]
MAX_RETRIES = 3
REGIONS = {
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

LOG_DIR = Path("logs") / "download_GTRENDS"
LOG_PATH = LOG_DIR / f"{datetime.now().isoformat()}.log"


def setup_logging() -> None:
    """Configure root logger to log to stdout and file."""
    LOG_DIR.mkdir(exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(LOG_PATH),
        ],
    )


def main():
    setup_logging()

    # Selenium Config
    options = Options()
    options.add_argument("--start-maximized")
    # options.add_argument("--headless")  # Activar si no necesitas ver el navegador
    service = Service(str(DRIVER_PATH))
    driver = webdriver.Chrome(service=service, options=options)
    wait = WebDriverWait(driver, 15)

    try:
        for term in TERMS:
            for region_name, region_code in REGIONS.items():
                attemp = 0
                success = False
                while attemp < MAX_RETRIES and not success:
                    attemp += 1
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
                        logging.info(f"Downloaded: {term} / {region_name}")
                        time.sleep(1)
                        success = True

                    except Exception as e:
                        msg = f"Attemp {attemp} failed: {type(e).__name__} - {str(e)}"
                        print(f"⚠️ {msg}")
                        if attemp == MAX_RETRIES:
                            print(f"❌ Downloaded failed for {term} / {region_name}")
                            logging.error(f"Download failed for {term} / {region_name}: {msg}")
                        else:
                            logging.warning(f"Attemp {attemp} failed for {term} / {region_name}")
                            time.sleep(1)
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
