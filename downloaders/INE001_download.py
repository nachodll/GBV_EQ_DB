import logging
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

DRIVER_PATH = Path("/opt/homebrew/bin/chromedriver")
URL = "https://www.ine.es/dynt3/inebase/index.htm?padre=525#"

LOG_DIR = Path("logs") / "download_INE"
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
    # options.add_argument("--headless")
    service = Service(str(DRIVER_PATH))
    driver = webdriver.Chrome(service=service, options=options)
    wait = WebDriverWait(driver, 15)

    try:
        driver.get(URL)

        # Wait untili download buttons are loaded
        try:
            wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a[title='Formatos de descarga disponibles']"))
            )
            print("📄 Download buttons were found")
        except TimeoutException:
            print("❌ Download buttons not found")
            logging.error("Download buttons not found")
            driver.quit()
            exit()

        # Find download buttons
        download_buttons = driver.find_elements(By.CSS_SELECTOR, "a[title='Formatos de descarga disponibles']")
        print(f"🔎 Found {len(download_buttons)} download buttons")

        for button in download_buttons:
            try:
                provincia_elem = button.find_element(By.XPATH, ".//ancestor::li//a[contains(@class, 'titulo')]")  # type: ignore
                provincia = provincia_elem.text.strip()
                print(f"\n➡️ Processing {provincia}")

                # Get direct link to pop up window
                popup_link = button.get_attribute("href")  # type: ignore
                driver.execute_script("window.open(arguments[0]);", popup_link)  # type: ignore
                driver.switch_to.window(driver.window_handles[-1])

                # Wait until pop up with file formats loads
                wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "ul.export li a")))
                formats = driver.find_elements(By.CSS_SELECTOR, "ul.export li a")
                csv_format = None
                for format in formats:
                    title = format.get_attribute("title")  # type: ignore
                    if title is not None and "CSV: separado por tabuladores" in title:
                        csv_format = format
                        break

                if csv_format:
                    href_csv = csv_format.get_attribute("href")  # type: ignore
                    if href_csv is not None:
                        driver.get(href_csv)
                        print(f"⬇️ Downloading CSV for {provincia}")
                        logging.info(f"Downloading CSV for {provincia}")
                        time.sleep(2)
                else:
                    print(f"❌ CSV format was not found for {provincia}")
                    logging.error(f"CSV format was not found for {provincia}")

                driver.close()
                driver.switch_to.window(driver.window_handles[0])

            except Exception as e:
                print(f"❌ Error processing: {e}")
                logging.error(f"Error processing: {e}")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
