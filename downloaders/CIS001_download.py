import logging
import os
import time
from datetime import datetime
from pathlib import Path

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

DRIVER_PATH = Path("/opt/homebrew/bin/chromedriver")
URL = "https://www.cis.es/catalogo-estudios/resultados-definidos/barometros"
CIS_EMAIL = os.getenv("CIS_EMAIL")


LOG_DIR = Path("logs") / "download_CIS"
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

        # Accept cookies
        try:
            wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "cn-ok"))).click()
            print("🍪 Cookies accepted")
        except Exception:
            print("ℹ️ No cookie banner found")

        # Load table
        wait.until(EC.presence_of_element_located((By.ID, "tablaEstudios")))
        estudio_urls = set()

        while True:
            print("🔄 Processing page...")
            wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "table#tablaEstudios tbody tr")))
            rows = driver.find_elements(By.CSS_SELECTOR, "table#tablaEstudios tbody tr")

            for row in rows:
                id_estudio = row.get_attribute("id")
                if id_estudio:
                    url_estudio = f"https://www.cis.es/es/detalle-ficha-estudio?idEstudio={id_estudio}"
                    estudio_urls.add(url_estudio)

            try:
                next_btn = driver.find_element(By.ID, "tablaEstudios_next")
                if "disabled" in next_btn.get_attribute("class"):
                    print("✅ Last page reached")
                    break
                else:
                    next_btn.click()
                    time.sleep(2)
            except Exception as e:
                print(f"❌ Not able to check next page: {e}")
                logging.error(f"Not able to check next page: {e}")
                break

        print(f"\n🔗 Total number of studies found: {len(estudio_urls)}")

        # Visit each study link
        for url in estudio_urls:
            try:
                print(f"\n➡️ Accessing: {url}")
                driver.get(url)
                time.sleep(2)

                try:
                    data_zip_link = driver.find_element(By.XPATH, "//a[contains(text(), 'Fichero datos')]")
                    print("📥 Data zip file available. Opening form...")
                    time.sleep(1)
                    driver.execute_script("arguments[0].click();", data_zip_link)
                except NoSuchElementException:
                    print("⚠️ No data zip file available for this study")
                    logging.warning(f"No data zip file available for {url}")
                    continue

                if len(driver.window_handles) > 1:
                    driver.switch_to.window(driver.window_handles[-1])

                wait.until(
                    EC.presence_of_element_located(
                        (By.XPATH, "//label[contains(., 'Email') and not(contains(., 'Confirmar'))]")
                    )
                )
                time.sleep(1)

                # Fill and submit form
                label_email = driver.find_element(
                    By.XPATH, "//label[contains(., 'Email') and not(contains(., 'Confirmar'))]"
                )
                input_email = driver.find_element(By.ID, label_email.get_attribute("for"))
                input_email.clear()
                input_email.send_keys(CIS_EMAIL)

                label_confirm = driver.find_element(By.XPATH, "//label[contains(., 'Confirmar Email')]")
                input_confirm = driver.find_element(By.ID, label_confirm.get_attribute("for"))
                input_confirm.clear()
                input_confirm.send_keys(CIS_EMAIL)

                try:
                    checkbox = driver.find_element(By.XPATH, "//label[contains(., 'acepta')]/input[@type='checkbox']")
                    checkbox.click()
                except NoSuchElementException:
                    try:
                        checkbox = driver.find_element(
                            By.XPATH, "//input[@type='checkbox' and contains(@name, 'Checkbox')]"
                        )
                        checkbox.click()
                    except Exception:
                        print("❌ Checkbox not found")
                        logging.error(f"Checkbox not found for {url}")
                        continue

                submit_btn = driver.find_element(By.ID, "ddm-form-submit")
                submit_btn.click()

                wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'Descargar')]")))
                download_btn = driver.find_element(By.XPATH, "//a[contains(text(),'Descargar')]")
                print(f"⬇️ Downloading from: {download_btn.get_attribute('href')}")
                download_btn.click()
                logging.info(f"Downloaded data for {url}")
                time.sleep(2)

                if len(driver.window_handles) > 1:
                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])

            except Exception as e:
                print(f"❌ Error processing {url}: {e}")
                logging.error(f"Error processing {url}: {e}")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
